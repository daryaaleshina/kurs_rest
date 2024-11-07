from django.db import models
from foods.models import Products

from users.models import User


class OrderitemQueryset(models.QuerySet):
    # суммарная стоимость
    def total_price(self):
        return sum(cart.products_price() for cart in self)
    
    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0


# модель записи заказа
class Order(models.Model):
    # пользователь, который сделал заказ
    user = models.ForeignKey(to=User, on_delete=models.SET_DEFAULT, blank=True, null=True, verbose_name="Пользователь", default=None)
    
    # дата создания заказа
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания заказа")
    
    # номер телефона пользователя
    phone_number = models.CharField(max_length=20, verbose_name="Номер телефона")
    
    # требуется ли доставка (true или false)
    requires_delivery = models.BooleanField(default=False, verbose_name="Требуется доставка")
    
    # адрес доставки
    delivery_address = models.TextField(null=True, blank=True, verbose_name="Адрес доставки")
    
    # оплата при получении? (true или false)
    payment_on_get = models.BooleanField(default=False, verbose_name="Оплата при получении")
    
    # оплачено ли? (true или false)
    is_paid = models.BooleanField(default=False, verbose_name="Оплачено")
    
    # статус заказа
    status = models.CharField(max_length=50, default='В обработке', verbose_name="Статус заказа")

    class Meta:
        db_table = "order"
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ("id",)

    def __str__(self):
        return f"Заказ № {self.pk} | Покупатель {self.user.first_name} {self.user.last_name}"

# сами заказанные блюда
class OrderItem(models.Model):
    # внешний ключ заказа
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE, verbose_name="Заказ")
    
    # заказанное блюдо
    product = models.ForeignKey(to=Products, on_delete=models.SET_DEFAULT, null=True, verbose_name="Блюдо", default=None)
    
    # название блюда
    name = models.CharField(max_length=150, verbose_name="Название")
    
    # цена заказа
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Цена")
    
    # количество заказанных блюд
    quantity = models.PositiveIntegerField(default=0, verbose_name="Количество")
    
    # дата продажи
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Дата продажи")


    class Meta:
        db_table = "order_item"
        verbose_name = "Проданное блюдо"
        verbose_name_plural = "Проданные блюда"
        ordering = ("id",)

    objects = OrderitemQueryset.as_manager()

    # суммарная цена
    def products_price(self):
        return round(self.price * self.quantity, 2)

    def __str__(self):
        return f"Блюдо {self.name} | Заказ № {self.order.pk}"
