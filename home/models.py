from django.db import models
from django.utils import timezone
from datetime import datetime

# Create your models here.
class Provider(models.Model):
	name = models.CharField(primary_key=True, max_length = 20)
	shortcut = models.CharField(max_length = 2, unique=True)
	logo = models.URLField()

class Visit(models.Model):
	provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
	dateOfVisit = models.DateTimeField(auto_now=True)
	user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
	floor = models.DecimalField(max_digits=2, decimal_places=0)
	
class Floor(models.Model):
	floor = models.DecimalField(max_digits=2, decimal_places=0)