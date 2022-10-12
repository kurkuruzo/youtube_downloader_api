from dataclasses import fields
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import YouTubeVideo


class YouTubeVideoSerializer(ModelSerializer):
    download_full_url = SerializerMethodField()
    
    class Meta:
        model = YouTubeVideo        
        fields = ['id', 'name', 'description', 'url', 'download_url', 'length', 'thumbnail', 'filesize_OK']
        
    def download_full_url(self, obj):
        return obj.download_url