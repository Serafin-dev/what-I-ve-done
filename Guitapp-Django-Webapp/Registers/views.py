from Gastos.models import *
from Tables.models import *
from User.models import Balance
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.models import User

# Create your views here.
# Index Page
@login_required(login_url='gastos:login')
def index(request):

   # Check if user 
   if not request.user.is_authenticated:
      return HttpResponseRedirect(reverse("gastos:login"))
   
   # POST
   if request.method == "POST":
      # month of the register
      month = timezone.now().strftime('%B')
      
      # If Outcome
      if request.POST['hidden'] == 'Outcome':
         
         form = OutcomeForm(request.POST)
         if form.is_valid():
            
            # Form Data
            d = form.cleaned_data
            
            # Get existing Categorie object
            c = Categories.objects.get_or_create(title=d["categorie"])
            
            # Create new Outcome
            outcome = Outcome( user = request.user,
                               creation_date = d['creation_date'], 
                               categorie = c[0], 
                               description = d['description'], 
                               outcome = d['outcome'] * (- 1), 
                               month = month )
            outcome.save()
            
            # Update user balance
            actual_balance = Balance.objects.get(user=request.user)
            new_value = actual_balance.value - d['outcome']
            new_balance = Balance.objects.update_or_create(user=request.user, defaults = {'value': new_value} )

         # FORM not valid or error
         else:
            return render(request, "Gastos/egresos.html", {
               "message" : "Form did not submit. Try again",
            })
   
      
      #If income
      else: 
         
         form = IncomeForm(request.POST)
         if form.is_valid():
            
            # form cleaned data
            d = form.cleaned_data          
            # Categorie object
            c = Income_categorie.objects.get_or_create(title=d["categorie"])
            
            # Create new Income 
            income = Income( user = request.user,
                             creation_date = d['creation_date'], 
                             categorie = c[0], 
                             description = d['description'], 
                             income = d['income'],  
                             month = month )
            income.save()

            # Update user balance
            actual_balance = Balance.objects.get(user=request.user)
            new_value = actual_balance.value + d['income']
            new_balance = Balance.objects.update_or_create(user=request.user, defaults = {'value': new_value} )

         # Form not valid or error
         else:

            return render(request, "Gastos/ingresos.html", {
               "message" : "Form did not submit. Try again",
            })
            
   #GET
   return render(request, "Gastos/index.html")

#Login #
def login_view(request):
   user_id = request.user.id
   if request.method == "POST":
       username = request.POST["username"]
       password = request.POST["password"]
       
       #authenticate user 
       user = authenticate(request, username=username, password=password)
       
       # if user exists 
       if user is not None:          
          
          # Login
          login(request, user)
          return HttpResponseRedirect(reverse("gastos:index"))
       
       # if user doesn't exist then error mssg
       else:
          return render(request, "Gastos/login.html", {
             "message": "Datos incorrectos"
          })
   return render(request, "Gastos/login.html")
#Logout #       
def logout_view(request):
   logout(request)  
   return render(request, "Gastos/login.html", {
      "message":"Te desconectaste"
   }) 

# Incomes
@login_required(login_url='gastos:login')
def incomes(request):
   return render(request, "Gastos/ingresos.html", {
      "incomeForm": IncomeForm()
   })

# Outcomes
@login_required(login_url='gastos:login')
def outcomes(request):
   return render(request, "Gastos/egresos.html", {
      "outcomeForm": OutcomeForm()
   })

#Register
def register(request):
   
   #POST
   if request.method == "POST":
      r_form = RegisterForm(request.POST)
      
      if r_form.is_valid():
         d = r_form.cleaned_data
         
         # Create User
         user = User.objects.create_user( first_name = d['first_name'],
                                          last_name = d['last_name'],
                                          username = d['first_name'],
                                          email = d['email'],
                                          password = d['password']
                                        )

         # if User was succesfully created                                        
         if user:
            # Session data
            request.session['first_name'] = user.first_name
            request.session['last_name'] = user.last_name
            request.session['username'] = user.username
            request.session['id'] = user.id
            request.session['email'] = user.email
            
            # Balance
            b = Balance(user = user, value = 0.00)
            b.save()
                        
            # Registration succesfull
            return render(request, "Gastos/login.html", {
               'message': "Your registration was succesfull. You can login now!\n Have a nice day."
            })

      #if form not valid
      return render(request, "Gastos/register.html", {
         'message':"Something went wrong with the data you provided",
         'form' : r_form
      })

   # GET
   return render (request, "Gastos/register.html",{
         'form' : RegisterForm()
   })
