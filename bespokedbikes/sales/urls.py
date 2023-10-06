from . import views
from django.urls import path

app_name = "sales"

urlpatterns = [
    path('', views.index, name='index'),
]