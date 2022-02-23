from Tables.models import Categories, Income_categorie
from django import forms

class OutcomeForm(forms.Form):
    # Structure
    creation_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), label=False)
    categorie = forms.ModelChoiceField( queryset=Categories.objects.all().order_by("title"), 
                                        label=False, 
                                        empty_label="Seleccione una categoria", 
                                        required=True )   

    description = forms.CharField(label=False, widget=forms.TextInput(attrs={'placeholder': 'Descripción...'}))
    outcome = forms.IntegerField(label=False, widget=forms.NumberInput(attrs={'placeholder': 'Gasté...'}))
    
    #hidden value to difference from IncomeForm in Template
    hidden = forms.CharField(widget=forms.TextInput(attrs={'type':'hidden', 'value':'Outcome'}))


class IncomeForm(forms.Form):
    #creation_date = forms.DateTimeField(label="creation_date")
    creation_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), label=False)
    categorie = forms.ModelChoiceField( queryset=Income_categorie.objects.all().order_by("title"), 
                                        label=False, 
                                        empty_label="Seleccione una categoria", 
                                        required=True )      

    description = forms.CharField( label=False, 
                                   widget=forms.TextInput(attrs={'placeholder': 'Descripción...'}))
    
    income = forms.IntegerField( label=False, 
                                 widget=forms.NumberInput(attrs={'placeholder': 'Ingresó...'}))
    #hidden input
    hidden = forms.CharField(widget=forms.TextInput(attrs={'type':'hidden', 'value':'Income'}))

class RegisterForm(forms.Form):
    first_name = forms.CharField( required = True,
                                  label = False, 
                                  max_length=20, 
                                  widget=forms.TextInput(attrs={'placeholder': 'First name...', 'type':'text'}))
    last_name = forms.CharField( required = True,
                                 label = False, 
                                 max_length=20, 
                                 widget=forms.TextInput(attrs={'placeholder': 'Last Name...', 'type':'text'}))
    email = forms.EmailField ( required = True, 
                               max_length=50, 
                               label = False,
                               widget=forms.TextInput(attrs={'placeholder': 'Email...', 'type':'email'}))
    password = forms.CharField( required = True,
                                label = False, 
                                max_length=50, 
                                widget=forms.TextInput(attrs={'placeholder': 'Password', 'type':'password'}))

#get data from Forms
def getDataFrom(form):
    d = form.cleaned_data
            # creation_date = form.cleaned_data["creation_date"]
            # categorie = form.cleaned_data["categorie"]
            # description = form.cleaned_data["description"]
            # outcome = form.cleaned_data["outcome"]
            # hidden = form.cleaned_data["hidden"]
            
            # return creation_date, categorie, description, outcome, hidden
    return d

