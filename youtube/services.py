import logging
import pytube
from typing import Optional
from django.utils import timezone
import youtube.config as config
from .models import YouTubeVideo
from .serializers import YouTubeVideoSerializer
from .tasks import download_video


logger = logging.getLogger(__name__)

def add_video(url: str):
    logger.info(f"STARTING ASYNC TASK FOR VIDEO {url}")
    video_in_db = _video_in_db(url)
    logger.info(f"{video_in_db=}")
    if video_in_db:
        return (video_in_db.id, None)
    
    yt_downloader = get_downloader(url=url)
    yt_video = create_video_obj(url=url, downloader=yt_downloader)
    logger.info(f"Created video {yt_video}")
    yt_video.path = yt_downloader.streams.get_highest_resolution().default_filename
    yt_video.save()
    
    logger.info(f"{yt_video.id=}")
    logger.info(f"{yt_video.name=}")
    logger.info(f"{yt_video.path=}")
    stream = yt_downloader.streams.get_highest_resolution()
    download_task = download_video.delay(stream)
    logger.info(f"{download_task=}")
    download_task_id = download_task.id
    return (yt_video.id, download_task_id)

def create_video_obj(url: str, downloader: pytube.YouTube) -> YouTubeVideo:
    video_obj = YouTubeVideo(name=downloader.title, description=downloader.description, url=url, length=downloader.length, date_added=timezone.now(), thumbnail=downloader.thumbnail_url)
    return video_obj
    
def _video_in_db(url: str) -> Optional[YouTubeVideo]:
    logger.info(f"Found video with url={url}, video object={YouTubeVideo.objects.filter(url=url).first()}")
    return YouTubeVideo.objects.filter(url=url).first()    
    
def get_downloader(url: str) -> pytube.YouTube:
    yt_downloader = pytube.YouTube(url, on_complete_callback=_download_completed, on_progress_callback=_download_progress)
    logger.info(yt_downloader)
    return yt_downloader

def _download_completed(stream: pytube.Stream, file_path: str) -> str:
    logger.info(f"{stream.title} download finished")
    return file_path

def _download_progress(stream: pytube.Stream, chunk, bytes_remaining):
    logger.info(
        f"{stream.title} progress: {round((1 - (bytes_remaining / stream.filesize)) * 100, 0)}%"
    )
 
    
def serialize_video(video: YouTubeVideo):
    return YouTubeVideoSerializer(video, many=False)