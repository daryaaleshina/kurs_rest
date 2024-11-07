from django.db import models

from users.models import User
from foods.models import Products

# класс для дополнительных методов корзины (для Итоговой суммы)
class CartQuerySet(models.QuerySet):
    # полная стоимость всех корзин пользователя
    def total_price(self):
        return sum(cart.foods_price() for cart in self)

    # подсчёт количества заказанных блюд
    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0
    


class Cart(models.Model):

    user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Пользователь')
    product = models.ForeignKey(to=Products, on_delete=models.CASCADE, verbose_name='Блюдо')
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name='Количество')
    session_key = models.CharField(max_length=32, null=True, blank=True)
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    class Meta:
        db_table = 'cart'
        verbose_name = "Корзина"
        verbose_name_plural = "Корзина"
        ordering = ("id",)

    objects = CartQuerySet().as_manager()

    # сколько будет стоить n-количество блюда
    def foods_price(self):
        return round(self.product.price * self.quantity, 2)

    def __str__(self):
        if self.user:
            return f'Корзина {self.user.username} | Блюдо {self.product.name} | Количество {self.quantity}'
        
        return f'Анонимная корзина | Блюдо {self.product.name} | Количество {self.quantity}'
