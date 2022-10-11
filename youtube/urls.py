from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("videos", views.VideosList.as_view(), name="videos"),
    path("video/details/<str:pk>/", views.VideoDetails.as_view(), name="video-details"),
    path("video/add-video", views.AddVideo.as_view(), name="add-video"),
    path("video/add-video-form", views.AddVideoForm.as_view(), name="add-video-form"),
    path("video/<str:pk>", views.GetVideo.as_view(), name="get-video"),
    path("video/url", views.GetVideoByUrl.as_view(), name="get-video-by-url"),
    path("video/status/", views.CheckDownloadStatus.as_view(), name="check-download-status"),
    path("video/confirmation/", views.confirmation, name="confirmation"),
]