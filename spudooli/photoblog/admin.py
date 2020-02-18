from django.contrib import admin
from .models import Post 

class PostAdmin(admin.ModelAdmin):
    list_display = ('headline', 'slug', 'status','datetime')
    list_filter = ("status",)
    search_fields = ['headline', 'body']
    prepopulated_fields = {'slug': ('headline',)}
  
admin.site.register(Post, PostAdmin)