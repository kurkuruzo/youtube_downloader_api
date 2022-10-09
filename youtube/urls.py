from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("videos", views.VideosList.as_view(), name="videos"),
    path("video-details/<str:pk>/", views.VideoDetails.as_view(), name="video-details"),
    path("add-video", views.AddVideo.as_view(), name="add-video"),
]