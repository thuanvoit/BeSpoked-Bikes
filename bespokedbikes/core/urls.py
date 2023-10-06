from . import views
from django.urls import path

app_name = "core"

urlpatterns = [
    path('', views.index, name='index'),
    path('salesperson/', views.salesperson, name='salesperson'),
    path('salesperson/update/<str:id>', views.update_salesperson, name="update_salesperson"),
    
]