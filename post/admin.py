from django.contrib import admin
from .models import Comment, Post, Profile
from django.contrib.auth.admin import UserAdmin


class CommentInline(admin.TabularInline):
    model = Comment
    max_num = 0
    fields = ['author', 'post']

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'post_date')
    inlines = [CommentInline]

class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'comment_date')

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'created')

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
