import logging
import pytube
from typing import Optional
from django.utils import timezone
import youtube.config as config
from .models import YouTubeVideo
from .serializers import YouTubeVideoSerializer


logger = logging.getLogger(__name__)


    
def serialize_video(video: YouTubeVideo):
    return YouTubeVideoSerializer(video, many=False)