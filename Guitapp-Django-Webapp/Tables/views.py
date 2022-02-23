from sre_parse import CATEGORIES
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from Gastos.models import *
from Gastos.views import incomes
from django.shortcuts import render 
from Tables.models import Categories

#Useful to Join iterables into a single element
from itertools import chain
from User.models import Balance

# Create your views here.
@login_required(login_url='gastos:login')
def index(request):
    username = request.user.first_name
    actualDate = timezone.now()
    actualMonth = actualDate.month
    actualMonthStart = actualDate.strftime('%B')
    
    # user balance
    balance = Balance.objects.get(user = request.user)
    # monthlyOutcomes = Outcome.objects.filter(creation_date_month = actualMonth)
    
    #weeks
    weeks = ["Semana 1", "Semana 2", "Semana 3", "Semana 4"]

    return render(request, "Tables/index.html",{
        'username': username,
        'balance' : balance,
        "weeks" : weeks,
        "actualDate" : actualDate,
        "actualMonthStart" : actualMonthStart,
        "actualMonth" : actualMonth,
        "username" : request.user.username,
        # "monthlyOutcomes" : monthlyOutcomes,        
        #deberia entregarle un array con los 12 meses llamado "meses"
    
    })
# categorie
@login_required(login_url='gastos:login')
def categorie(request, categorie_id):
    user_id = request.user.id
    categorie = Categories.objects.get(pk=categorie_id)

    c_outcomes = (categorie.outcomes.filter(user_id=user_id))

    return render(request, "Tables/categorie.html", {
        "categorie" : categorie, 
        "c_outcomes": c_outcomes,
    })
# Incomes
@login_required(login_url='gastos:login')
def incomes(request, categorie_id):
    user_id = request.user.id
    categorie = Income_categorie.objects.get(pk=categorie_id)

    c_incomes = categorie.incomes.filter(user_id=user_id)
    return render(request, "Tables/incomes.html", {
        "categorie" : categorie, 
        "c_incomes": c_incomes,
    })

# Outcomes
@login_required(login_url='gastos:login')
def outcomes(request):
    return render(request, "Tables/outcomes.html")


# Monthly Income view
from django.views.generic.dates import MonthArchiveView
from datetime import datetime
class MonthlyIncomes(MonthArchiveView):

            # class properties
            template_name = 'Tables/monthly_incomes.html'
            date_field = 'creation_date'
            # allows future dates in objects
            allow_future = True
            # specifies whether to display the page (instead of raising a 404) if no objects are available 
            # in "queryset" context variable
            allow_empty = True

            # override queryset context variable 
            # (queryset must be provided as a parameter when using MonthArchiveView) 
            def get_queryset(self):
                category = Income_categorie.objects.get(pk=self.kwargs['categorie_id'])
                queryset = category.incomes.filter(user=self.request.user) 
                return queryset
            
            # additional context data    
            def get_context_data(self, **kwargs):
                context = super().get_context_data(**kwargs)
                user_id = self.request.user.id
                context['category'] = Income_categorie.objects.get(pk=self.kwargs['categorie_id'])
                context['c_incomes'] = context['category'].incomes.filter(user_id=user_id)
                context['year'] = context['month'].strftime("%Y")
                context['abb_prev_month'] = context['previous_month'].strftime("%B")[:3]
                context['abb_next_month'] = context['next_month'].strftime("%B")[:3]

                # Total incomes for the month
                context['month_total'] = 0
                for register in context['object_list']:
                    context['month_total'] += register.income
                
                # change year when accesing December from Jan
                if context['abb_prev_month'] == 'Dec' and context['month'].strftime('%B')[:3] == 'Jan':
                    context['year'] = str(int(context['year']) - 1)
                
                # change year when accesing Jan from Dec
                elif context['abb_next_month'] == 'Jan' and context['month'].strftime('%B')[:3] == 'Dec':
                    context['year'] = str(int(context['year']) + 1)
                

                return context

# Monthly Outcome view
class MonthlyOutcomes(MonthArchiveView):

            # class properties
            template_name = 'Tables/monthly_outcomes.html'
            date_field = 'creation_date'
            allow_future = True
            allow_empty = True
            
            def get_queryset(self):
                category = Categories.objects.get(pk=self.kwargs['categorie_id'])
                queryset = category.outcomes.filter(user=self.request.user) 
                return queryset
    