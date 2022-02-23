#To create a path to a specific url first import "path" function from django.urls class.
from django.urls import path
#import views file to use its functions.
from . import views
#"urlpatterns" variable keeps all the urls available for this particular app.
app_name = 'gastos'
urlpatterns = [
    # Views represent views.py and index is the function we wrote on it.
    # The string name at the end of the path represents the url path.
    #when we go to the default route Example: "" = mysite.com/defaultRoute 
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("register", views.register, name="register"),
    path("logout", views.logout_view, name="logout"),
    path("incomes", views.incomes, name="incomes"),
    path("outcomes", views.outcomes, name="outcomes"),
    #path("<str:name>", views.saludarUsuario, name="saludar")#
]
