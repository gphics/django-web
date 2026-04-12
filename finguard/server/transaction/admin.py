from django.contrib import admin
from .models import Transaction, Category, Circle, CircleMembership

# Register your models here.
admin.site.register(Transaction)
admin.site.register(Category)
admin.site.register(Circle)
admin.site.register(CircleMembership)