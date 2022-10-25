from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("videos", views.VideosList.as_view(), name="videos"),
    path("videos/<str:pk>", views.VideoDetails.as_view(), name="video-details"),
    path("videos/", views.AddVideoForm.as_view(), name="add-video-form"),
    path("videos/url", views.GetVideoByUrl.as_view(), name="get-video-by-url"),
    path("videos/confirmation", views.confirmation, name="confirmation"),
    path("api/videos", views.AddVideo.as_view(), name="add-video"),
    path("api/videos/status", views.CheckDownloadStatus.as_view(), name="check-download-status"),
    path("api/videos/<str:pk>", views.GetVideo.as_view(), name="get-video"),
]