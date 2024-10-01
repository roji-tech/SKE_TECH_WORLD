from django.contrib import admin

# Register your models here.
from .models import BlogPost, Tag


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['headline', "created", "updated", "is_public"]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', "id",]
