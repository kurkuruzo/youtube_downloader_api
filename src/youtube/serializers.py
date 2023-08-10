from rest_framework.serializers import ModelSerializer, Serializer, CharField
from .models import DownloadRequest, YouTubeVideo


class YouTubeVideoSerializer(ModelSerializer):
    class Meta:
        model = YouTubeVideo
        fields = ['id', 'name', 'description', 'url', 'download_url', 'length', 'thumbnail', 'abs_path', 'filesize_OK']


class DownloadRequestSerializer(ModelSerializer):
    class Meta:
        model = DownloadRequest
        fields = ["id", "video", "status"]

    video = YouTubeVideoSerializer()

class DownloadTaskResultSerializer(Serializer):
    video_id = CharField()
    path = CharField()


class DownloadTaskserializer(Serializer):
    id = CharField()
    result = DownloadTaskResultSerializer()
