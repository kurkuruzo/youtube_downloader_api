from django.contrib import admin

from .models import YouTubeVideo

class YouTubeVideoAdmin(admin.ModelAdmin):
    # list_display = ['id', 'title']
    pass

# Register your models here.
admin.site.register(YouTubeVideo, YouTubeVideoAdmin)
# admin.site.register(YouTubeVideoAdmin)