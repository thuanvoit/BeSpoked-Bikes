from django.contrib import admin

# Register your models here.

from .models import Sale, Customer, Product, Salesperson, Discount

admin.site.register(Sale)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Salesperson)
admin.site.register(Discount)
