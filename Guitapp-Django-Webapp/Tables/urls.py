from django.urls import path
from .views import *

app_name = "tables"
urlpatterns = [
    path("", index, name="index"),
    #path("outcomes", views.outcomes, name="outcomes"), 
    path("<int:categorie_id>", categorie, name="categorie"),
    path("incomes/<int:categorie_id>/", incomes, name = "incomes"),
    #path for monthly incomes categorie view
    path("incomes/<int:categorie_id>/<int:year>/<str:month>/", MonthlyIncomes.as_view(), name="monthly_incomes"),
    #path for monthly outcomes categorie view
    path("<int:categorie_id>/<int:year>/<str:month>/", MonthlyOutcomes.as_view(), name="monthly_outcomes"),
]