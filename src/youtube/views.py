from ast import Return
from celery.result import AsyncResult
from django.utils import timezone
from django.shortcuts import render, redirect, resolve_url
from django.views import generic, View
import logging
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from youtube import serializers
from .models import DownloadRequest, TelegramDownloadRequest, YouTubeVideo
from .tasks import download_video

import youtube.services as services

logger = logging.getLogger(__name__)

# Create your views here.
def home(request):
    return render(request=request, template_name="youtube/home.html")


def confirmation(request):
    video_id = request.GET.get("video_id")
    download_task_id = request.GET.get("download_task_id")
    logger.info(f"{video_id=}")
    logger.info(f"{download_task_id=}")
    video_obj = YouTubeVideo.get_by_id(video_id)
    return render(
        request=request,
        template_name="youtube/confirmation.html",
        context={"download_task_id": download_task_id, "video": video_obj},
    )


class VideosList(generic.ListView):
    model = YouTubeVideo
    template_name: str = "youtube/list.html"
    ordering = ("-date_added",)


class VideoDetails(generic.DetailView):
    model = YouTubeVideo
    template_name: str = "youtube/detail.html"


class AddVideoForm(View):
    def post(self, request, *args, **kwargs):
        url = request.POST.get("url")
        logger.info(f"{url=}")
        try:
            video_id, download_task_id = services.add_video(url)
        except services.YouTubeError as e:
            logger.exception(e)
            return render(request=request, template_name="youtube/error.html", context={"error": e})
        return redirect(
            f"{resolve_url('confirmation')}?download_task_id={download_task_id}&video_id={video_id}"
        )

# API Views
class AddVideo(APIView):
    def post(self, request, format=None) -> Response:
        logger.info(request.data)
        url = request.data.get("url")
        chat_id = request.data.get("chat_id")
        message_id = request.data.get("message_id")
        logger.info(f"{url=}")
        
        if not url:
            return Response({"error": "No url provided"})
        
        # request = TelegramDownloadRequest(url=url, date_added=timezone.now(), chat_id=chat_id, message_id=message_id) if chat_id and message_id else DownloadRequest(url=url, date_added=timezone.now())
        if chat_id and message_id:
            request, _ = TelegramDownloadRequest.objects.get_or_create(url=url, date_added=timezone.now(), chat_id=chat_id, message_id=message_id)
        else:
            request, _ = DownloadRequest.objects.get_or_create(url=url, date_added=timezone.now())
        try:
            request.video = services.add_video(url)
        except services.YouTubeError as e:
            logger.exception(e)
            return Response({"error": e})
        request.save()
        # download_task = services.download_video(request.video)
        if request.video.filesize_OK:
            return Response({"request_id": request.id, "video_id": request.video.id, "status": "FINISHED"})
        download_task: AsyncResult = download_video.delay(download_request=request)
        request.status = download_task.status
        if request.status == "FAILURE":
            return Response({"error": "Failed to download video"})
        elif request.status == "SUCCESS":
            services.send_successful_download_confirmation(request.video, chat_id, message_id)
        return Response({"request_id": request.id, "video_id": request.video.id, "download_task_id": download_task.id, "status": request.status})

class DownloadedVideosView(generics.ListAPIView):
    queryset = DownloadRequest.objects.filter(status="SUCCESS")
    serializer_class = serializers.DownloadRequestSerializer


class CheckDownloadStatus(generics.RetrieveAPIView):
    serializer_class = serializers.DownloadTaskserializer

    def get_object(self):
        task_id = self.kwargs.get("pk")
        logger.info(f"{task_id=}")
        if task_id:
            res = AsyncResult(task_id)
            logger.info(f"{res.__dict__=}")
            logger.info({"status": res.state})
            logger.info({"status": res.result})
            return res


class GetVideo(generics.RetrieveAPIView):
    queryset = YouTubeVideo.objects.all()
    serializer_class = serializers.YouTubeVideoSerializer


class SetVideoDownoaded(generics.UpdateAPIView):
    queryset = DownloadRequest.objects.all()
    serializer_class = serializers.DownloadRequestSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = "COMPLETE"
        instance.save()
        return Response(self.get_serializer(instance).data.get("id"))


class GetVideoByUrl(generics.RetrieveAPIView):
    # queryset = YouTubeVideo.objects.all()
    serializer_class = serializers.YouTubeVideoSerializer

    def get_queryset(self):
        queryset = YouTubeVideo.objects.all()
        url = self.request.GET.get("url")
        if url:
            queryset = queryset.filter(url=url)
        return queryset
