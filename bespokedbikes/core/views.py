import json
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import *
from .forms import *
from django.shortcuts import get_object_or_404

from django.db.models import Min, Max
from .utils import *

def index(request):
    return render(request, "core/base.html")

def salesperson_view(request):
    data = Salesperson.objects.all()
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
        "data": data,
    }, status=status_code)

def salesperson_update(request, id):
    salesperson_data = Salesperson.objects.get(id = id)
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
    }, status=status_code)

def product_update(request, id):
    product_data = Product.objects.get(id = id)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product_data)
        if form.is_valid():
            try:
                form.save()
                return redirect(reverse("core:product"))
            except IntegrityError:
                form.add_error(None, "Product with this name and manufacturer already exists.")
    else:
        form = ProductForm(instance=product_data)
        
    return render(request, "core/product_update.html", {
        "form": form,
        "data": product_data,
    })

def customer_view(request):
    data = Customer.objects.all()
    return render(request, "core/customer.html", {
        "data": data,
    })

def sale_view(request):
    data = Sale.objects.all()
    
    oldest_date = format_date(Sale.objects.aggregate(oldest_date=Min('sales_date'))['oldest_date'])
    nearest_date = format_date(Sale.objects.aggregate(nearest_date=Max('sales_date'))['nearest_date'])
    
    start_date = oldest_date
    end_date = nearest_date
    
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        data = Sale.objects.filter(sales_date__gte=start_date, sales_date__lte=end_date)
        
    return render(request, "core/sale.html", {
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
        product = Product.objects.get(id = request.POST.get('product'))
        salesperson = Salesperson.objects.get(id = request.POST.get('salesperson'))
        customer = Customer.objects.get(id = request.POST.get('customer'))
        sales_date = format_date(request.POST.get('sales_date'))
        price = request.POST.get('price')
        salesperson_commission = request.POST.get('salesperson_commission')
        
        new_sale = Sale(product=product,
                        salesperson=salesperson,
                        customer=customer,
                        sales_date=sales_date,
                        price=price,
                        salesperson_commission=salesperson_commission)
        new_sale.save()
    
    return render(request, "core/sale_create.html", {
        "products": products,
        "salesperson": salespersons,
        "customers": customers,
    })
    
def discount_list(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        print(data)
    except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    return JsonResponse({'error': 'Unsupported HTTP method'}, status=405)