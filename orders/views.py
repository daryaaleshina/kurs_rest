from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.forms import ValidationError
from django.shortcuts import redirect, render

from carts.models import Cart

from orders.forms import CreateOrderForm
from orders.models import Order, OrderItem

@login_required
def create_order(request):
    if (
        request.method == "POST"
    ):  # если нажата кнопка Оформить заказ на странице оформления заказа
        # получаем данные из формы
        form = CreateOrderForm(data=request.POST)

        if form.is_valid():  # если данные в форме введены корректно
            with transaction.atomic():  # в рамках одного пакета транзакций, которые должны быть исполнены БД
                user = request.user  # получаем данные пользователя
                cart_items = Cart.objects.filter(
                    user=user
                )  # выбираем все корзины, которые есть у пользователя
                if cart_items.exists():  # если корзины существуют
                    # создаём заказ
                    order = Order.objects.create(
                        user=user,
                        phone_number=form.cleaned_data["phone_number"],
                        requires_delivery=form.cleaned_data["requires_delivery"],
                        delivery_address=form.cleaned_data["delivery_address"],
                        payment_on_get=form.cleaned_data["payment_on_get"],
                    )
                    # создаём заказанные блюда
                    for cart_item in cart_items:
                        product = cart_item.product
                        name = cart_item.product.name
                        price = cart_item.product.price
                        quantity = cart_item.quantity

                        OrderItem.objects.create(
                            order=order,
                            product=product,
                            name=name,
                            price=price,
                            quantity=quantity,
                        )
                        product.save()

                    # очищаем корзину пользователя после создания заказа
                    cart_items.delete()

                    messages.success(request, "Заказ оформлен!")
                    return redirect("user:profile")

    else:  # если не POST запрос
        # предзаполненные данные
        initial = {
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
        }

        form = CreateOrderForm(
            initial=initial
        )  # инициализируем форму дефолтными значениями

    context = {
        "title": "Luxury - Оформление заказа",
        "form": form,
        "order": True,
    }
    return render(request, "orders/create_order.html", context=context)
