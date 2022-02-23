from django.utils import timezone
from django.db import models
from Tables.models import *
from django.contrib.auth.models import User
# User model
#current date
current_date = timezone.now()

# Create your models here
class Outcome(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='outcomes')
    creation_date = models.DateField(auto_now_add=True)
    categorie = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name="outcomes")
    description = models.CharField(default="", max_length=30)
    outcome = models.IntegerField()  
    month = models.CharField(default="", max_length=30)   

    def __str__(self):
        return f"{self.creation_date}: {self.categorie}: {self.description}: {self.outcome}: {self.month}"
    

class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='incomes')
    creation_date = models.DateField(auto_now_add=True)
    categorie = models.ForeignKey(Income_categorie, on_delete=models.CASCADE, related_name="incomes")
    description = models.CharField(default="", max_length=30)
    income = models.IntegerField()
    month = models.CharField(default="",max_length=30)   

    def __str__(self):
        return f"{self.creation_date}: {self.categorie}: {self.description}: {self.income}: {self.month}"

