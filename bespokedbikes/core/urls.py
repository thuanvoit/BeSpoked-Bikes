from . import views
from django.urls import path

app_name = "core"

urlpatterns = [
    path('', views.index, name='index'),
    # salesperson
    path('salesperson/', views.salesperson_view, name='salesperson'),
    path('salesperson/update/<str:id>', views.salesperson_update, name="salesperson_update"),
    # product
    path('product/', views.product_view, name='product'),
    path('product/update/<str:id>', views.product_update, name="product_update"),
    # customer
    path('customer/', views.customer_view, name='customer'),
    
    
]