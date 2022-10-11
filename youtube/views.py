from celery.result import AsyncResult
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.views import generic
from django.http import HttpResponseNotFound
import logging

from youtube import serializers
from .models import YouTubeVideo
from .services import serialize_video
from .tasks import add_video
from rest_framework.views import APIView
from rest_framework import generics
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
    

class AddVideo(APIView):
    def post(self, request, format=None):
        logger.info(request.data)
        url = request.data.get('url')
        logger.info(f"{url=}")
        res = add_video.delay(url=url)
        return Response(res.id)
        # return Response(serialize_video(video).data)
        
class CheckDownloadStatus(APIView):
    def get(self, request):
        task_id = request.GET.get('task_id')
        logger.info(f"{task_id=}")
        if task_id:
            res = AsyncResult(task_id)
            return Response({'status': res.state, 'uuid': res.result})
        return HttpResponseNotFound()
    
# class GetVideo(generics.RetrieveAPIView):
#     def get(self, request, pk, format=None):
#         logger.info(f"{pk=}")
#         if not pk:
#             return HttpResponseNotFound()
#         try:
#             video = YouTubeVideo.get_by_id(id=pk)
#         except ValidationError as e:
#             return (HttpResponseNotFound(e))
#         return Response(serialize_video(video).data)

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