from re import U
from django.contrib import admin

from carts.admin import CartTabAdmin
from orders.admin import OrderTabulareAdmin
from users.models import User

# admin.site.register(User)
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "first_name", "last_name", "email",]

    # поля для поиска
    search_fields = ["username", "first_name", "last_name", "email",]

    # поле для привязки у пользователя его корзины
    inlines = [CartTabAdmin, OrderTabulareAdmin]