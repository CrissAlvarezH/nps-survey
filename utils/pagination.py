import math

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class UbietyPagination(PageNumberPagination):
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response({
            'pagination_data': {
                'links': {
                    'next': self.get_next_link(),
                    'previous': self.get_previous_link()
                },
                'total_pages': (
                    math.ceil(
                        self.page.paginator.count / self.get_page_size(self.request)
                    )
                ),
                'on_page': len(self.page),
                'page': self.page.number,
                'count': self.page.paginator.count,
            },
            'results': data
        })
