
# ver1
from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_size_query_param = "limit"
    page_size = 6


# from rest_framework.pagination import PageNumberPagination

# from .constants import PAGINATION_PAGE_SIZE


# class FoodgramPagination(PageNumberPagination):
#     """ Пагинация для проекта Фудграм. """
#     page_size = PAGINATION_PAGE_SIZE
#     page_size_query_param = 'limit'
