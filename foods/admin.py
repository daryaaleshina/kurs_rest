from django.contrib import admin

from foods.models import Categories, Products

# admin.site.register(Categories)
# admin.site.register(Products)

@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ["name",]

# панель администратора (блюд)
@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

    list_display = ["name", "price"]
    search_fields = ["name", "description"] # по каким полям будет производится поиск
    list_filter = ["category"] # фильтрация для категории
    # порядок распреления полей отдельных блюд
    fields = [
        "name",
        "category",
        "slug",
        "description",
        "image",
        "price", 
    ]
