from django.contrib import admin

from web.models import Post, New, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "text", "date", "author")
    search_fields = ("id", "title")
    list_filter = ("id", "date")
    ordering = ("-date",)


class NewAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "date", "author", "photo")
    search_fields = ("id", "title")
    list_filter = ("id", "date")
    ordering = ("-date",)


class CommentAdmin(admin.ModelAdmin):

    
    list_display = ("id", "text", "post_id", "date")
    search_fields = ("id", "title", "post_id")
    list_filter = ("id", "post_id", "date")
    ordering = ("-date",)


admin.site.register(Post, PostAdmin)
admin.site.register(New, NewAdmin)
admin.site.register(Comment, CommentAdmin)
