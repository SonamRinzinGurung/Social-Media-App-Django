from django.contrib import admin
from . models import User, Posts,Likes,Follow


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email',)

class PostsAdmin(admin.ModelAdmin):
    list_display = ('post', 'created_by', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('post', 'created_by')
    ordering = ('-created_at',)

admin.site.register(User, UserAdmin)
admin.site.register(Posts,PostsAdmin)
admin.site.register(Likes)
admin.site.register(Follow)