from django.db import models
from django.forms import ValidationError

class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.TextField()
    phone = models.CharField(max_length=20, unique=True, blank=False)
    start_date = models.DateField()
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Salesperson(models.Model):
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    address = models.TextField(blank=False)
    phone = models.CharField(max_length=20, blank=False, unique=True)
    start_date = models.DateField()
    termination_date = models.DateField(null=True, blank=True)
    manager = models.CharField(max_length=100, blank=False)
    
    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
    def clean(self):
        super().clean()

        if self.start_date and self.termination_date and self.start_date > self.termination_date:
            raise ValidationError("Termination date must be later than the start date.")
    

class Product(models.Model):
    name = models.CharField(max_length=100, blank=False)
    manufacturer = models.CharField(max_length=100, blank=False)
    style = models.CharField(max_length=50, blank=False, default="Other")
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    qty_on_hand = models.PositiveIntegerField()
    commission_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    
    class Meta:
        unique_together = ('name', 'manufacturer')

    def __str__(self):
        return f"{self.name} by {self.manufacturer} ${self.sale_price}"

class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    salesperson = models.ForeignKey(Salesperson, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    sales_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    salesperson_commission = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return f"{self.product.name} ${self.price} - Orig: ${self.product.sale_price} {'DISCOUNTED' if self.price == self.product.sale_price else ''}"

class Discount(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    begin_date = models.DateField()
    end_date = models.DateField()
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    
    def __str__(self):
        return f"{self.product.name} by {self.product.manufacturer} - {self.discount_percentage}"
