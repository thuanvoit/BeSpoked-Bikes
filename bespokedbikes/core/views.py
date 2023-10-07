import json
from django.db import IntegrityError, connection
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import *
from .forms import *
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.db.models.functions import ExtractYear, ExtractMonth
from django.db.models import Sum, Count
from django.core.paginator import Paginator
from .query import *

from django.db.models import Min, Max
from .utils import *


def index(request):
    return render(request, "core/apps.html", {
        "apps_link": get_apps_link()
    })


def salesperson_view(request):
    data = Salesperson.objects.all()
    paginator = Paginator(data, 50)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    if data:
        error = ""
        msg = "Retrieve data successfully"
        status_code = 200
    else:
        error = "Error retrieve data"
        msg = ""
        status_code = 404
    return render(request, "core/salesperson.html", {
        "error": error,
        "msg": msg,
        "data": page,
        "apps_link": get_apps_link()
    }, status=status_code)


def salesperson_update(request, id):
    salesperson_data = Salesperson.objects.get(id=id)
    if request.method == 'POST':
        form = SalespersonForm(request.POST, instance=salesperson_data)
        if form.is_valid():
            form.save()
            return redirect(reverse("core:salesperson"))
    else:
        form = SalespersonForm(instance=salesperson_data)

    return render(request, "core/salesperson_update.html", {
        "form": form,
        "data": salesperson_data,
        "apps_link": get_apps_link()
    })


def product_view(request):
    data = Product.objects.all()
    
    paginator = Paginator(data, 50)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    
    if data:
        error = ""
        msg = "Retrieve data successfully"
        status_code = 200
    else:
        error = "Error retrieve data"
        msg = ""
        status_code = 404
    return render(request, "core/product.html", {
        "error": error,
        "msg": msg,
        "data": page,
        "apps_link": get_apps_link()
    }, status=status_code)


def product_update(request, id):
    product_data = Product.objects.get(id=id)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product_data)
        if form.is_valid():
            try:
                form.save()
                return redirect(reverse("core:product"))
            except IntegrityError:
                form.add_error(
                    None, "Product with this name and manufacturer already exists.")
    else:
        form = ProductForm(instance=product_data)

    return render(request, "core/product_update.html", {
        "form": form,
        "data": product_data,
        "apps_link": get_apps_link()
    })


def customer_view(request):
    data = Customer.objects.all()
    paginator = Paginator(data, 50)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, "core/customer.html", {
        "data": page,
        "apps_link": get_apps_link()
    })


def sale_view(request):
    data = execute_custom_query(query_all_sales)
        
    oldest_date = format_date(Sale.objects.aggregate(
        oldest_date=Min('sales_date'))['oldest_date'])
    nearest_date = format_date(Sale.objects.aggregate(
        nearest_date=Max('sales_date'))['nearest_date'])
    
    start_date = oldest_date
    end_date = nearest_date

    if request.method == 'POST':
        
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        data = execute_custom_query(query_sale_by_date_range, 
                                    [start_date, end_date])

    paginator = Paginator(data, 50)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    
    return render(request, "core/sale.html", {
        "apps_link": get_apps_link(),
        "data": page,
        "start_date": start_date,
        "end_date": end_date,
        "oldest_date": oldest_date,
        "nearest_date": nearest_date
    })


def create_sale(request):
    products = Product.objects.filter(qty_on_hand__gt=0)
    salespersons = []
    customers = []

    if request.method == 'POST':
        print(request.POST)
        product = Product.objects.get(id=request.POST.get('product'))
        salesperson = Salesperson.objects.get(id=request.POST.get('salesperson'))
        customer = Customer.objects.get(id=request.POST.get('customer'))
        sales_date = format_date(request.POST.get('sales_date'))
       
        discounts = Discount.objects.filter(
            product=product,
            begin_date__lte=sales_date,
            end_date__gte=sales_date,
        )
        max_discount = discounts.order_by('-discount_percentage').first()

        if discounts:
            product_price = sale_calculate(product.sale_price,
                                           max_discount.discount_percentage,
                                           product.commission_percentage)
        else:
            product_price = sale_calculate(product.sale_price,
                                           0,
                                           product.commission_percentage)

        new_sale = Sale(product=product,
                        salesperson=salesperson,
                        customer=customer,
                        sales_date=sales_date,
                        price=product_price["sale_price"],
                        salesperson_commission=product_price["commission"])
        
        new_sale.save()
        
        qty = int(product.qty_on_hand)
        print(product.qty_on_hand)
        product.qty_on_hand = qty - 1
        print(product.qty_on_hand)
        product.save()
            
        return redirect(reverse("core:sale"))

    return render(request, "core/sale_create.html", {
        "apps_link": get_apps_link(),
        "products": products,
        "salesperson": salespersons,
        "customers": customers,
    })


def sale_report(request):
    stats = []

    year_range_query = Sale.objects.aggregate(min_year=Min(ExtractYear('sales_date')),
                                              max_year=Max(ExtractYear('sales_date')))

    min_year = year_range_query['min_year']
    max_year = year_range_query['max_year']

    if request.method == 'POST':
        year = int(request.POST.get('year'))
        quarter = int(request.POST.get('quarter'))
        
        print(year, quarter)

        query = """
            SELECT sp.id AS salesperson_id, sp.first_name, sp.last_name, 
                sp.phone as phone, ROUND(SUM(s.price)) AS revenue, 
                ROUND(SUM(s.salesperson_commission), 2) AS commission, 
                COUNT(s.product_id) AS total_product, s.sales_date, 
                (cast(strftime('%%m', s.sales_date) as integer) + 2) / 3 as quarter,
                (cast(strftime('%%Y', s.sales_date) as integer)) as year
                
            FROM core_salesperson AS sp 
            LEFT JOIN core_sale AS s ON s.salesperson_id = sp.id
            
            WHERE year = %s AND quarter = %s
            GROUP BY sp.id;
        """

        # Execute the raw SQL query
        with connection.cursor() as cursor:
            cursor.execute(query, [year, quarter])
            stats = cursor.fetchall()
            cursor.close()

    paginator = Paginator(stats, 50)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    
    return render(request, "core/sale_report.html", {
        "apps_link": get_apps_link(),
        "year_range": range(min_year, max_year + 1),
        "stats": page
    })


def seed_sample(request):
    clean_data()
    add_sample_data()
    return HttpResponse("Feed data successfully.")

@csrf_exempt
def saler_details(request):
    if request.method == 'POST':
        raw_data = request.body
        data_str = raw_data.decode('utf-8')
        data = json.loads(data_str)
        sales_date = data['sale_date']
        data = execute_custom_query(query_saler_by_sale_date, 
                                    [sales_date, sales_date])
        return JsonResponse(data, status=200, safe=False)
    else:
        return JsonResponse({'error': 'Unsupported HTTP method'}, status=405)

@csrf_exempt
def customer_details(request):
    if request.method == 'POST':
        raw_data = request.body
        data_str = raw_data.decode('utf-8')
        data = json.loads(data_str)
        sales_date = data['sale_date']
        data = execute_custom_query(query_customer_by_sale_date, 
                                    [sales_date])
        return JsonResponse(data, status=200, safe=False)
    else:
        return JsonResponse({'error': 'Unsupported HTTP method'}, status=405)
  
@csrf_exempt
def product_details(request):
    if request.method == 'POST':
        raw_data = request.body
        data_str = raw_data.decode('utf-8')
        data = json.loads(data_str)
        sales_date = data['sale_date']
        
        print(sales_date, data['id'])
        
        product = Product.objects.get(id=data['id'])

        discounts = Discount.objects.filter(
            product=product,
            begin_date__lte=sales_date,
            end_date__gte=sales_date,
        )
        max_discount = discounts.order_by('-discount_percentage').first()

        if discounts:
            product_price = sale_calculate(product.sale_price,
                                           max_discount.discount_percentage,
                                           product.commission_percentage)
        else:
            product_price = sale_calculate(product.sale_price,
                                           0,
                                           product.commission_percentage)

        return JsonResponse(product_price, status=200, safe=False)
    else:
        return JsonResponse({'error': 'Unsupported HTTP method'}, status=405)
