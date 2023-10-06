from django.contrib import admin

# Register your models here.

from sales.models import Sale
from customer.models import Customer
from product.models import Product
from salesperson.models import Salesperson
from discount.models import Discount

admin.site.register(Sale)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Salesperson)
admin.site.register(Discount)
