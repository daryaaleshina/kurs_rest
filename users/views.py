from email import message
from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from carts.models import Cart
from orders.models import Order, OrderItem
from django.db.models import Prefetch
from orders.models import Order
from users.forms import ProfileForm, UserLoginForm, UserRegistrationForm

# Авторизация
def login(request):

    if request.method == 'POST': # нажата кнопка Войти формы Авторизация
        form = UserLoginForm(data=request.POST)
        if form.is_valid(): # если данные введены корректно
            username = request.POST['username']
            password =   request.POST['password']
            # проверка, есть ли пользователь с таким именем и паролем
            user = auth.authenticate(username=username, password=password)

            # получаем сессионный ключ
            session_key = request.session.session_key

            if user: # если есть пользователь с таким именем и паролем
                auth.login(request, user) # логинем пользователя
                messages.success(request, f"{username}, Вы вошли в аккаунт")

                if session_key: # если есть сессионный ключ
                    Cart.objects.filter(session_key=session_key).update(user=user)
                    
                redirect_page = request.POST.get('next', None)
                if redirect_page and redirect_page != reverse('user:logout'):
                    return HttpResponseRedirect(request.POST.get('next'))
                return HttpResponseRedirect(reverse('main:index'))# возвращаем пользователя на главную страницу
    else: # формирование формы Авторизация при нажатии кнопки Войти на главном банере
        form = UserLoginForm()

    context={
        'title': 'Luxury - Авторизация',
        'form': form
    }
    return render(request, 'users/login.html', context)

# Регистрация
def registration(request):
    if request.method == 'POST': # нажата кнопка Зарегестрироваться
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid(): # если данные введены корректно
            form.save() # заносим введённые данные в БД

            # получаем сессионный ключ
            session_key = request.session.session_key

            users = form.instance
            auth.login(request, users)

            if session_key: # если есть сессионный ключ
                    Cart.objects.filter(session_key=session_key).update(user=users)

            messages.success(request, f"{form.instance.username}, Вы успешно зарегестрированы")
            return HttpResponseRedirect(reverse('user:login'))# возвращаем пользователя на страницу авторизации
    else: # формирование формы Регистрации при нажатии кнопки Создать аккаунт
        form = UserRegistrationForm()

    context={
        'title': 'Luxury - Регистрация',
        'form': form
    }
    return render(request, 'users/registration.html', context)


# Вход в личный кабинет пользователя
@login_required
def profile(request):
    if request.method == 'POST': # нажата кнопка Сохранить
        form = ProfileForm(data=request.POST, instance=request.user, files=request.FILES)
        if form.is_valid(): # если данные введены корректно
            form.save() # заносим введённые данные в БД
            messages.success(request, "Данные успешно обновлены")
            return HttpResponseRedirect(reverse('user:profile'))
    else: # формирование формы Регистрации при нажатии кнопки Создать аккаунт
        form = ProfileForm(instance=request.user)

    # заказы пользователя
    orders = Order.objects.filter(user=request.user).prefetch_related(
                Prefetch(
                    "orderitem_set",
                    queryset=OrderItem.objects.select_related("product"),
                )
            ).order_by("-id")

    context={
        'title': 'Luxury - Кабинет',
        'form': form,
        'orders': orders
    }
    return render(request, 'users/profile.html', context)

# корзина (на главном банере)
def users_cart(request):
    return render(request, 'users/users_cart.html')

# Выход из кабинета
@login_required
def logout(request):
    messages.success(request, f"{request.user.username}, Вы вышли из аккаунта")
    auth.logout(request)
    return redirect(reverse('main:index'))
