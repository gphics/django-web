from django.contrib import admin
from .models import Post, Comment

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "slug"]
    list_filter = ["created", "status"]
    prepopulated_fields = {"slug":("title", )}
    show_facets = admin.ShowFacets.ALWAYS


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["name", "post", "created"]
    list_filter = ["name", "created"]
    show_facets = admin.ShowFacets.ALWAYS