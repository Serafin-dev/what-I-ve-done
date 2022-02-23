from django.db.models.lookups import In
from Gastos.models import Income, Outcome
from django.contrib import admin

# Register your models here.
admin.site.register(Outcome)
admin.site.register(Income)
