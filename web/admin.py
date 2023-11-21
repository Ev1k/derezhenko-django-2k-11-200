from django.contrib import admin

from web.models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "text", "date", "author")
    search_fields = ("id", "title")
    ordering = "-date"


admin.site.register(Post)
