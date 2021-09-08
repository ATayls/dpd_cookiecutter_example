from django.contrib import admin

from dpd_cc_example.example.models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'slug',
        'summary',
        'body',
        'created_on',
        'status',
    )
    list_filter = ('created_on',)
    search_fields = ('slug',)
