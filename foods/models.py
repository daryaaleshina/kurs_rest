from unicodedata import category
from django.db import models
from django.urls import reverse

# Описание таблицы с помощью модели
class Categories(models.Model):
    # id создаётся автоматически (settings.py - DEFAULT_AUTO_FIELD)

    # категории (текстовая информация)
    name = models.CharField(max_length=150, unique=True, verbose_name='Название')

    # фрагмент url-адреса
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')

    # изменения
    class Meta:
        db_table = 'category'
        verbose_name ='Категорию'
        verbose_name_plural = 'Категории'
        ordering = ("id",)

    def __str__(self):
        return self.name

    
# таблица с информацией о блюдах
class Products(models.Model):
    # название блюда (текстовая информация)
    name = models.CharField(max_length=150, unique=True, verbose_name='Название')

    # фрагмент url-адреса
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')

    # описание
    description = models.TextField(blank=True, null=True, verbose_name='Описание')

    # изображение
    image = models.ImageField(upload_to='foods_images', blank=True, null=True, verbose_name='Изображение')

    # цена
    price = models.DecimalField(default=0.00, max_digits=7, decimal_places=2, verbose_name='Цена')

    # какая категория продукта (связь с таблицей Категории)
    category = models.ForeignKey(to=Categories, on_delete=models.CASCADE, verbose_name='Категория')

    

    # изменения
    class Meta:
        db_table = 'product'
        verbose_name ='Блюдо'
        verbose_name_plural = 'Блюда'
        ordering=("id",)

    def __str__(self):
        return self.name
    
    # для создания url маршрутов
    def get_absolute_url(self):
        return reverse("catalog:product", kwargs={"product_slug": self.slug})

