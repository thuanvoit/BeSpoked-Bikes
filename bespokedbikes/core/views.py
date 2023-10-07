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
        "data": data,
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
    return render(request, "core/customer.html", {
        "data": data,
        "apps_link": get_apps_link()
    })


def sale_view(request):
    data = Sale.objects.all()

    oldest_date = format_date(Sale.objects.aggregate(
        oldest_date=Min('sales_date'))['oldest_date'])
    nearest_date = format_date(Sale.objects.aggregate(
        nearest_date=Max('sales_date'))['nearest_date'])

    start_date = oldest_date
    end_date = nearest_date

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        data = Sale.objects.filter(
            sales_date__gte=start_date, sales_date__lte=end_date)

    return render(request, "core/sale.html", {
        "apps_link": get_apps_link(),
        "data": data,
        "start_date": start_date,
        "end_date": end_date,
        "oldest_date": oldest_date,
        "nearest_date": nearest_date
    })


def create_sale(request):
    products = Product.objects.all()
    salespersons = Salesperson.objects.all()
    customers = Customer.objects.all()

    if request.method == 'POST':
        product = Product.objects.get(id=request.POST.get('product'))
        salesperson = Salesperson.objects.get(
            id=request.POST.get('salesperson'))
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

        if quarter == 1:
            start_month = 1
            end_month = 3
            end_date = 31
        elif quarter == 2:
            start_month = 4
            end_month = 6
            end_date = 30
        elif quarter == 3:
            start_month = 7
            end_month = 9
            end_date = 30
        elif quarter == 4:
            start_month = 10
            end_month = 12
            end_date = 31

        query = """
            SELECT sp.id AS salesperson_id, sp.first_name, sp.last_name, 
                sp.phone as phone, ROUND(SUM(s.price)) AS revenue, 
                ROUND(SUM(s.salesperson_commission), 2) AS commission, 
                COUNT(s.product_id) AS total_product, s.sales_date
            FROM core_salesperson AS sp 
            LEFT JOIN core_sale AS s ON s.salesperson_id = sp.id
            WHERE s.sales_date >= %s AND s.sales_date <= %s
            GROUP BY sp.id;
        """

        # Define the date range
        start_date = f"{year}-{start_month}-01"
        end_date = f"{year}-{end_month}-{end_date}"

        # Execute the raw SQL query
        with connection.cursor() as cursor:
            cursor.execute(query, [start_date, end_date])
            stats = cursor.fetchall()

    return render(request, "core/sale_report.html", {
        "apps_link": get_apps_link(),
        "year_range": range(min_year, max_year + 1),
        "stats": stats
    })


def seed_sample(request):
    clean_data()
    add_sample_data()
    return HttpResponse("Feed data successfully.")


@csrf_exempt
def product_details(request):
    if request.method == 'POST':
        raw_data = request.body
        data_str = raw_data.decode('utf-8')
        data = json.loads(data_str)
        sales_date = data['sale_date']
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
