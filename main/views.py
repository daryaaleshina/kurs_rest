
from django.http import HttpResponse
from django.shortcuts import render

from foods.models import Categories

# Главная страница
def index(request):

    context = {
        'title': 'Luxury - Главная',
        'content': "Ресторан Luxury",
    }
    
    return render(request, 'main/index.html', context)

# Страница вывода информации
def about(request):
    context = {
        'title': 'Luxury - О нас',  
    }
    
    return render(request, 'main/about.html', context)
