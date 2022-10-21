from dataclasses import fields
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import YouTubeVideo


class YouTubeVideoSerializer(ModelSerializer):
    class Meta:
        model = YouTubeVideo        
        fields = ['id', 'name', 'description', 'url', 'download_url', 'length', 'thumbnail', 'filesize_OK']
        