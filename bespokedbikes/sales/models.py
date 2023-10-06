from django.db import models

from product.models import Product
from salesperson.models import Salesperson
from customer.models import Customer

class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    salesperson = models.ForeignKey(Salesperson, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    sales_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    salesperson_commission = models.DecimalField(max_digits=10, decimal_places=2)


