from django.shortcuts import render
from django.views import generic
from .models import YouTubeVideo
from .services import add_video
from rest_framework.views import APIView
from rest_framework.response import Response

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
    def get(self, request, formant=None):
        url = request.GET.get('url')
        video = add_video(url)
        return Response(f'<a href="{video.url}">{video.name}</a> : {video.path}')