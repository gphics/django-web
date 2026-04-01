from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from utils.res import generate_res


class TransactionPagination(PageNumberPagination):
    """
    This is a custom pagination built to handle user transactions
    """

    def get_paginated_response(self, data):
        result = {
            "next": self.get_next_link(),
            "previous":self.get_previous_link(),
            "count":self.page.paginator.count,
            "total_pages":self.page.paginator.num_pages,
            "current_page":self.page.number,
            "transactions": data
        }
        return Response(
            generate_res(result)
        )