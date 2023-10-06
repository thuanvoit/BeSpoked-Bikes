from . import views
from django.urls import path

app_name = "customer"

urlpatterns = [
    path('', views.index, name='index'),
]