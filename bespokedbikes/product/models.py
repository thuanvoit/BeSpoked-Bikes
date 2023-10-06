from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    style = models.CharField(max_length=50)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    qty_on_hand = models.PositiveIntegerField()
    commission_percentage = models.DecimalField(max_digits=5, decimal_places=2)
