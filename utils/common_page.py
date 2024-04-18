# xing
# xing
from rest_framework.pagination import PageNumberPagination


class MyPageNumberPagination(PageNumberPagination):
    page_size = 10  # default page size
    page_query_param = 'page'  # 前端发送的页数关键字名，默认为”page”
    page_size_query_param = 'size'  # 前端发送的每页数目关键字名，默认为None
    max_page_size = 10000  # max page size
