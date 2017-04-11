from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField('date created', auto_now_add=True)
class Developer(models.Model):
    user = models.OnetoOneField(User,on_delete=models.CASCADE)

