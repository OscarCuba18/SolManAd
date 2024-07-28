from django.contrib import admin
from .models import Comment

class Comment_Admin(admin.ModelAdmin):
    list_display = ('request_id', 'user_id', 'comment', 'date_added')

admin.site.register(Comment, Comment_Admin)
