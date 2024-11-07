import re
from django.db.models import Q
from django.contrib.postgres.search import SearchVector,SearchQuery,SearchRank,SearchHeadline

from foods.models import Products


def q_search(query):

    # поиск по ключевым словам (и по названию, и по описанию блюда)

    # сортировка запроса по релевантности
    vector = SearchVector("name", "description")
    query = SearchQuery(query)

    result = (
        Products.objects.annotate(rank=SearchRank(vector, query))
        .filter(rank__gt=0)
        .order_by("-rank")
    )

    result = result.annotate(
        headline=SearchHeadline(
            "name",
            query,
            start_sel='<span style="background-color: yellow;">',
            stop_sel="</span>",
        )
    )

    result = result.annotate(
        bodyline=SearchHeadline(
            "description",
            query,
            start_sel='<span style="background-color: yellow;">',
            stop_sel="</span>",
        )
    )

    return result
