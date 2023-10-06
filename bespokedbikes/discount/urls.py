from . import views
from django.urls import path

app_name = "discount"

urlpatterns = [
    path('', views.index, name='index'),
]