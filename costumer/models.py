from django.db import models

# Create your models here.
class Costumer(models.Model):
    costumer_name = models.CharField(max_length=30)
    email_costumer = models.CharField(max_length=30)
    phone_costumer = models.CharField(max_length=30)
    gender_costumer = models.CharField(max_length=30)
    decription = models.CharField(max_length=30)