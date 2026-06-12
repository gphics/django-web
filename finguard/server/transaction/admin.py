from django.contrib import admin
from .models import Transaction, Category, Circle, CircleMembership, CircleInvite

# Register your models here.
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_filter = ("flagged", "transaction_type")
    list_display = ("user","category", "transaction_date", "amount")
    pass
admin.site.register(Category)
admin.site.register(Circle)
admin.site.register(CircleInvite)
admin.site.register(CircleMembership)