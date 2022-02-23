from Tables.models import Categories
from Gastos.models import *
from itertools import chain

def add_variable_to_layout(request):
    #session
    #user_id = request.session["id"]
    user_id = request.user.id

    # Select all outcomes, incomes and categories from User
    outcomes = Outcome.objects.filter(user_id = user_id)
    incomes = Income.objects.filter(user_id = user_id)
    categories = Categories.objects.all()
    
    return {
        'categori_url' : "Tables/categorie.html",
        'categories': categories,
        'outcomes' : outcomes,
        'incomes' : incomes,
        'registers' : list(chain(outcomes, incomes)),
    }

def outcome_sidenav_buttons(request):

    icon_urls = {}
    # Outcome Categories
    d = Categories.objects.all()
    # icon urls
    urls = ['https://img.icons8.com/external-vitaliy-gorbachev-flat-vitaly-gorbachev/58/000000/external-bread-oktoberfest-vitaliy-gorbachev-flat-vitaly-gorbachev.png',   
            'https://img.icons8.com/external-becris-lineal-color-becris/64/000000/external-education-literary-genres-becris-lineal-color-becris.png',
            'https://img.icons8.com/plasticine/100/000000/exercise.png',
            'https://img.icons8.com/doodle/96/000000/popcorn.png', 
            'https://img.icons8.com/dusk/64/000000/heart-health.png',
            'https://img.icons8.com/office/80/000000/taxi.png',
            'https://img.icons8.com/color/96/000000/clothes.png',     
            'https://img.icons8.com/external-kiranshastry-lineal-color-kiranshastry/64/000000/external-more-interface-kiranshastry-lineal-color-kiranshastry.png',
            'https://img.icons8.com/color/48/000000/light.png',
            ]
    # Outcome categories urls
    c_urls = ['/tables/1', '/tables/2', '/tables/3', '/tables/4', '/tables/5', '/tables/6', '/tables/7', '/tables/8', '/tables/9']
    for i in range(len(d)):
            icon_urls[c_urls[i]] = urls[i]
    
    return {
            'urls': urls,
            'icon_urls' : icon_urls,
    }

def income_sidenav_buttons(request):
        c_data = {}
        # Income categories
        d = Income_categorie.objects.all()
        
        # icon urls
        i_urls = ['https://img.icons8.com/external-bearicons-blue-bearicons/64/000000/external-Sale-discount-day-bearicons-blue-bearicons.png',
                  'https://img.icons8.com/external-icongeek26-linear-colour-icongeek26/64/000000/external-boss-due-diligence-icongeek26-linear-colour-icongeek26-1.png',
                  'https://img.icons8.com/external-sbts2018-lineal-color-sbts2018/58/000000/external-freelance-work-from-home-sbts2018-lineal-color-sbts2018.png',
                  'https://img.icons8.com/external-ddara-lineal-color-ddara/64/000000/external-rental-real-estate-ddara-lineal-color-ddara.png',
                  'https://img.icons8.com/external-kiranshastry-lineal-color-kiranshastry/64/000000/external-more-interface-kiranshastry-lineal-color-kiranshastry.png',      
        ]
        
        # Income categories urls
        c_urls = ['/tables/incomes/1', '/tables/incomes/2', '/tables/incomes/3', '/tables/incomes/4', '/tables/incomes/5']        
        
        for i in range(len(d)):
            c_data[c_urls[i]] = i_urls[i]   
        
        return{ 
                'c_data' : c_data             
        }