from django import template
from django.utils.http import urlencode
from foods.models import Categories

# регистрация шаблонного тэга
register = template.Library()

@register.simple_tag()
def tag_categories():
    # категории блюд из БД
    return Categories.objects.all()

# takes_context=True  - все контекстные переменные (request и прочие) будут 
# доступны через параметр context
@register.simple_tag(takes_context=True)
def change_params(context, **kwargs):
    query = context['request'].GET.dict()
    query.update(kwargs)
    return urlencode(query)
