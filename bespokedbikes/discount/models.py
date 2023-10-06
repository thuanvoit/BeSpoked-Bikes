from django.db import models
from product.models import Product

class Discount(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    begin_date = models.DateField()
    end_date = models.DateField()
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)