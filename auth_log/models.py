from django.db import models

# Create your models here.
class Users(models.Model):
    fname = models.CharField(max_length=30)
    lname = models.CharField(max_length=30)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=144)
