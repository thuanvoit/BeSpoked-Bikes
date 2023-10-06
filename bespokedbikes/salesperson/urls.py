from . import views
from django.urls import path

app_name = "salesperson"

urlpatterns = [
    path('', views.index, name='index'),
]