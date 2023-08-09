from django.contrib import admin

from .models import DownloadRequest, YouTubeVideo

class YouTubeVideoAdmin(admin.ModelAdmin):
    # list_display = ['id', 'title']
    pass

class DownloadRequestAdmin(admin.ModelAdmin):
    pass

# Register your models here.
admin.site.register(YouTubeVideo, YouTubeVideoAdmin)
admin.site.register(DownloadRequest, DownloadRequestAdmin)
# admin.site.register(YouTubeVideoAdmin)