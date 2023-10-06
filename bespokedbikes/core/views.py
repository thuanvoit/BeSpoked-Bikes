from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import *
from .forms import *

# Create your views here.
def index(request):
    # add_sample_data()
    return render(request, "core/base.html")

def salesperson_view(request):
    data = Salesperson.objects.all()
    return render(request, "core/salesperson.html", {
        "data": data,
    })

def salesperson_update(request, id):
    salesperson_data = Salesperson.objects.get(id = id)
    if request.method == 'POST':
        form = SalespersonForm(request.POST, instance=salesperson_data)
        if form.is_valid():
            form.save()
            return redirect(reverse("core:salesperson"))
        else:
            # DO STUFF HERE
            print("not valid")
        
    return render(request, "core/salesperson_update.html", {
        "data": salesperson_data,
    })

def product_view(request):
    data = Product.objects.all()
    return render(request, "core/product.html", {
        "data": data,
    })

def product_update(request, id):
    product_data = Product.objects.get(id = id)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product_data)
        if form.is_valid():
            form.save()
            return redirect(reverse("core:product"))
        else:
            # DO STUFF HERE
            print("not valid")
        
        
    return render(request, "core/product_update.html", {
        "data": product_data,
    })

def customer_view(request):
    data = Customer.objects.all()
    return render(request, "core/customer.html", {
        "data": data,
    })