from django.db import models
from django.utils import timezone

current_date = timezone.now()
# Create your models here.

class Categories(models.Model):
    title = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.title}"

class Income_categorie(models.Model):
    title = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.title}"

class Month(models.Model):
    name = models.CharField(max_length= 30)

    def __str__(self):
        return f"{self.name}"

