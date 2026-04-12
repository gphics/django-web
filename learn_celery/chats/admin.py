from django.contrib import admin
from .models import Comment, Post, Like
# Register your models here.
admin.site.register(Like)
@admin.register(Post)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["id","author"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["post"]
