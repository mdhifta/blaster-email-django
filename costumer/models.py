from django.db import models

# Create your models here.
class Costumer(models.Model):
    costumer_name = models.CharField(max_length=144)
    email_costumer = models.CharField(max_length=144)
    phone_costumer = models.CharField(max_length=13)
    gender_costumer = models.CharField(max_length=15)
    decription = models.CharField(max_length=144)
