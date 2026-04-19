from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'post_type', 'carbs_per_serving', 'created_at')
    list_filter = ('post_type', 'created_at', 'glycemic_index')
    search_fields = ('title', 'content')
    
    fieldsets = (
        (None, {
            'fields': ('title', 'content', 'post_type')
        }),
        ('Recipe Nutritional Info', {
            'classes': ('collapse',),
            'fields': ('carbs_per_serving', 'fiber', 'glycemic_index'),
            'description': 'Only fill these for Recipe posts.'
        }),
    )
