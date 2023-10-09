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
    # sales
    path('sale/', views.sale_view, name='sale'),
    # sales create
    path('sale/new', views.create_sale, name="new_sale"),
    # quarterly report
    path('sale_report/', views.sale_report, name="sale_report"),
    
    
    #
    # REST API
    path('api/product-details/', views.product_details, name="product_details"),
    path('api/saler-details/', views.saler_details, name="saler_details"),
    path('api/customer-details/', views.customer_details, name="customer_details"),

    
    # samples
    path('seed_sample/', views.seed_sample, name="seed_sample"),
    path('small_sample/', views.small_sample, name="small_sample"),

]