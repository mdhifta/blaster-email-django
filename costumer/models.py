from django.db import models

# Create your models here.
class Form(models.Model):
    costumer_name = models.CharField(max_length=60)
    email_costumer = models.CharField(max_length=30)
    phone_costumer = models.CharField(max_length=14)
    gender_costumer = models.CharField(max_length=30)
    decription = models.CharField(max_length=144)