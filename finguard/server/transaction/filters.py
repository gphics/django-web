import django_filters
from . models import Transaction


class TransactionFilter(django_filters.FilterSet):
    # category
    category = django_filters.CharFilter(field_name="category__title", lookup_expr="icontains")

    flagged = django_filters.BooleanFilter(field_name="flagged")

    transaction_type = django_filters.CharFilter(field_name="transaction_type", lookup_expr="icontains")

    # amount
    min_amount = django_filters.NumberFilter(field_name="amount", lookup_expr="gte")
    max_amount = django_filters.NumberFilter(field_name="amount", lookup_expr="lte")

    # transaction date
    year = django_filters.NumberFilter(field_name="transaction_date", lookup_expr="year")
    month = django_filters.NumberFilter(field_name="transaction_date", lookup_expr="month")


    class Meta:
        model = Transaction
        fields = ["category", "min_amount", "max_amount", "year", "month", "transaction_type", "flagged"]
