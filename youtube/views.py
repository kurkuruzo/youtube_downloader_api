from celery.result import AsyncResult
from django.shortcuts import render, redirect, resolve_url
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.views import generic, View
from django.http import HttpResponseNotFound
import logging
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response

from youtube import serializers
from .models import YouTubeVideo
import youtube.services as services
import youtube.producer as producer 

logger = logging.getLogger(__name__)

# Create your views here.
def home(request):
    producer.send_download_confirmation("1234235")
    return render(request=request, template_name='youtube/home.html')

def confirmation(request):
    video_id = request.GET.get('video_id')
    download_task_id = request.GET.get('download_task_id')
    logger.info(f"{video_id=}")
    logger.info(f"{download_task_id=}")
    video_obj = YouTubeVideo.get_by_id(video_id)
    return render(request=request, template_name='youtube/confirmation.html', context={'download_task_id': download_task_id, "video": video_obj})


class VideosList(generic.ListView):
    model = YouTubeVideo
    template_name: str = "youtube/list.html"
    ordering = ('-date_added',)

class VideoDetails(generic.DetailView):
    model = YouTubeVideo
    template_name: str = "youtube/detail.html"
    
    
class AddVideoForm(View):
    def post(self, request, *args, **kwargs):
        url = request.POST.get('url')
        logger.info(f"{url=}")
        video_id, download_task_id = services.add_video(url)
        return redirect(f"{resolve_url('confirmation')}?download_task_id={download_task_id}&video_id={video_id}")
      

class AddVideo(APIView):
    def post(self, request, format=None):
        logger.info(request.data)
        url = request.data.get('url')
        chat_id = request.data.get('chat_id')
        message_id = request.data.get('message_id')
        logger.info(f"{url=}")
        video_id, download_task_id = services.add_video(url, chat_id, message_id)
        return Response({'video_id': video_id, 'download_task_id': download_task_id})

class CheckDownloadStatus(APIView):
    def get(self, request):
        task_id = request.GET.get('task_id')
        logger.info(f"{task_id=}")
        if task_id:
            res = AsyncResult(task_id)
            logger.info(f"{res.__dict__=}")
            logger.info({'status': res.state})
            if res.state == "FAILURE":
                return HttpResponseNotFound(res)
            if res.state == "SUCCESS":
                return Response({'status': res.state, 'id': res.id})
            return Response({'status': res.state})
        return HttpResponseNotFound()
    

class GetVideo(generics.RetrieveAPIView):
    queryset = YouTubeVideo.objects.all()
    serializer_class = serializers.YouTubeVideoSerializer
    

class GetVideoByUrl(generics.RetrieveAPIView):
    # queryset = YouTubeVideo.objects.all()
    serializer_class = serializers.YouTubeVideoSerializer
    
    def get_queryset(self):
        queryset = YouTubeVideo.objects.all()
        url = self.request.GET.get('url')
        if url:
            queryset = queryset.filter(url=url)
        return queryset