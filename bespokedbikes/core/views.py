from django.http import HttpResponse
from django.shortcuts import render
from .models import *

# Create your views here.
def index(request):
    # add_sample_data()
    return render(request, "core/base.html")

def salesperson(request):
    data = Salesperson.objects.all()
    return render(request, "core/salesperson.html", {
        "data": data,
    })

def update_salesperson(request, id):
    return HttpResponse(id)


