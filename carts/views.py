from django.http import JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse
from carts.models import Cart
from carts.utils import get_user_carts
from foods.models import Products

# добавление блюда в корзину
def cart_add(request):
    
    product_id = request.POST.get("product_id")

    product = Products.objects.get(id=product_id)

    # если пользователь авторизован
    if request.user.is_authenticated:
        # получаем все корзины по определенному блюду
        carts = Cart.objects.filter(user=request.user, product=product)

        # если блюдо уже добавлено в корзину
        if carts.exists():
            cart = carts.first()
            if cart:
                cart.quantity += 1
                cart.save()
        else: # если в корзине нет ещё такого блюда
            Cart.objects.create(user=request.user, product=product, quantity=1)
    else: # если пользователь не авторизован 
        carts = Cart.objects.filter(
            session_key=request.session.session_key, product=product)

        if carts.exists(): # если корзина уже есть (не авториз. пользователь добавил блюдо уже)
            cart = carts.first()
            if cart:
                cart.quantity += 1
                cart.save()
        else: # иначе создаем корзину с одним блюдом
            Cart.objects.create(
                session_key=request.session.session_key, product=product, quantity=1)


    user_cart = get_user_carts(request)
    cart_items_html = render_to_string(
        "carts/includes/included_cart.html", {"carts": user_cart}, request=request)

    response_data = {
        "message": "Блюдо добавлено в корзину",
        "cart_items_html": cart_items_html,
    }

    return JsonResponse(response_data)

# изменение количества блюд в корзине
def cart_change(request):
    cart_id = request.POST.get("cart_id") 
    quantity = request.POST.get("quantity") # количество блюд после +1 или -1

    cart = Cart.objects.get(id=cart_id)

    cart.quantity = quantity
    cart.save()
    updated_quantity = cart.quantity

    user_cart = get_user_carts(request)

    context = {"carts": user_cart}

    # if referer page is create_order add key orders: True to context
    referer = request.META.get('HTTP_REFERER')
    if reverse('orders:create_order') in referer:
        context["order"] = True

    cart_items_html = render_to_string(
        "carts/includes/included_cart.html", context, request=request)

    response_data = {
        "message": "Количество изменено",
        "cart_items_html": cart_items_html,
        "quantity": updated_quantity,
    }

    return JsonResponse(response_data)

# удаление блюда из корзины
def cart_remove(request) -> JsonResponse:
    
    cart_id = request.POST.get("cart_id")

    cart: Cart = Cart.objects.get(id=cart_id) # экзмпляр корзины по id
    quantity = cart.quantity # количество блюд в корзине
    cart.delete()
    
    user_cart = get_user_carts(request) # вся корзина пользователя
    
    context = {"carts": user_cart}

    # if referer page is create_order add key orders: True to context
    referer = request.META.get('HTTP_REFERER')
    if reverse('orders:create_order') in referer:
        context["order"] = True
    
    cart_items_html = render_to_string(
        "carts/includes/included_cart.html", context, request=request)

    response_data = {
        "message": "Блюдо удалено",
        "cart_items_html": cart_items_html,
        "quantity_deleted": quantity,
    }

    return JsonResponse(response_data)