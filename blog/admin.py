from django.contrib import admin
from blog.models import Post, Tag, Comment


class CommentAdmin(admin.ModelAdmin):
    raw_id_fields = ("post", "author")
    list_display = ("id", "post", "author")
    
class PostAdmin(admin.ModelAdmin):
    raw_id_fields = ('tags', 'likes')
    list_display = ("id", "title", "author")  
    
admin.site.register(Post, PostAdmin)
admin.site.register(Tag)
admin.site.register(Comment, CommentAdmin)
