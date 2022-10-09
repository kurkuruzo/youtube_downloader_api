from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic
import logging
from .models import YouTubeVideo
from .services import add_video
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response

logger = logging.getLogger(__name__)

# Create your views here.
def home(request):
    return render(request=request, template_name='youtube/home.html')


class VideosList(generic.ListView):
    model = YouTubeVideo
    template_name: str = "youtube/list.html"
    ordering = ('-date_added',)

class VideoDetails(generic.DetailView):
    model = YouTubeVideo
    template_name: str = "youtube/detail.html"
    
    
# class AddVideo(APIView):
#     def get(self, request, formant=None):
#         url = request.GET.get('url')
#         video = add_video(url)
#         return Response(f'<a href="{video.url}">{video.name}</a> : {video.path}')

class AddVideo(APIView):
    def post(self, request, format=None):
        logger.info(request.data)
        url = request.data.get('url')
        logger.info(f"{url=}")
        video = add_video(url)
        return redirect(reverse("video-details", args=[video.id]))