import logging
import pytube
from django.utils import timezone
import youtube.config as config
from .models import YouTubeVideo

logger = logging.getLogger(__name__)

def add_video(url):
    yt_downloader, yt_video = _get_info(url, on_complete_callback=_download_completed)
    file_path = _download_video(yt_downloader)
    yt_video.path = yt_downloader.streams.get_highest_resolution().default_filename
    yt_video.save()
    return yt_video
        

def _get_info(url, **kwargs):
    yt_downloader = pytube.YouTube(url, on_complete_callback=_download_completed)
    logger.info(yt_downloader)
    yt_video = YouTubeVideo(name=yt_downloader.title, description=yt_downloader.description, url=url, length=yt_downloader.length, date_added=timezone.now(), thumbnail=yt_downloader.thumbnail_url)
    return yt_downloader, yt_video
    
    

def _download_video(video: pytube.YouTube, download_path=config.DOWNLOAD_PATH, skip_existing=True):
    logger.info(f"Downloading video: {video.title}")
    file_path = video.streams.get_highest_resolution().download(output_path=download_path, skip_existing=skip_existing)
    logger.info(f"Video {video.title} saved to {file_path}")
    return video.streams.get_highest_resolution().download(output_path=download_path, skip_existing=skip_existing)
    
    
def _download_completed(stream: pytube.Stream, file_path):
    logger.info(f"{stream.title} download finished")
    return file_path