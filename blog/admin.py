from django.contrib import admin

# Register your models here.

from .models import Author, Tag, Post, Comments

class PostAdmin(admin.ModelAdmin):
    list_filter = ("author", "date", "tags")
    list_display = ("title", "author", "date")
    prepopulated_fields = {"slug": ("title",)}

class CommentsAdmin(admin.ModelAdmin):
    list_filter = ("post", "date")
    list_display = ("name", "post", "date")

admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Post, PostAdmin)
admin.site.register(Comments, CommentsAdmin)