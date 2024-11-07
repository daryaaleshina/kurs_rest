from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render

from foods.models import Products
from foods.utils import q_search


# Контроллер каталога
def catalog(request, category_slug=None):
    # получение из request страницы
    page = request.GET.get('page', 1)

    # получение из request статус Фильтрации
    order_by = request.GET.get('order_by', None)

    # поиск
    query = request.GET.get('q', None)

    if category_slug == 'all':
        # получение всех блюд из БД
        foods = Products.objects.all()
    elif query:
        foods = q_search(query)
    else:
        # иначе по внешнему ключю category через filter получаем slug нужных продуктов категории
        foods = Products.objects.filter(category__slug=category_slug)
        if not foods.exists():
            raise Http404()

    # фильтрация по стоимости
    if order_by and order_by != "default":
        foods = foods.order_by(order_by)
    
    # пагинация (постраничная навигация) (6 блюд на странице)
    paginator = Paginator(foods, 6)

    # текущая страница 
    current_page = paginator.page(int(page))

    
    context = {
        "title": "Luxury - Каталог",
        "foods": current_page,
        "slug_url": category_slug,
    }

    return render(request, "foods/catalog.html", context)


# Контроллер отдельного блюда
def product(request, product_slug):

    # получаем информация о конкретном блюде из БД по id
    product = Products.objects.get(slug=product_slug)

    context = {
        'product': product
    }

    return render(request, "foods/product.html", context = context)
