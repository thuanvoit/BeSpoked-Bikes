from django.db import models

# Create your models here.
class Salesperson(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    start_date = models.DateField()
    termination_date = models.DateField(null=True, blank=True)
    manager = models.CharField(max_length=100)
