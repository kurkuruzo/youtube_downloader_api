from asyncio import streams
import logging
import pytube
from typing import Optional
from django.utils import timezone
import youtube.config as config
from .models import YouTubeVideo

logger = logging.getLogger(__name__)

def add_video(url: str) -> YouTubeVideo:
    video_in_db = _video_in_db(url)
    if video_in_db:
        return video_in_db
    yt_downloader = _get_info(url)
    yt_video = _create_video_obj(url=url, yt_downloader=yt_downloader)
    yt_video.path = yt_downloader.streams.get_highest_resolution().default_filename
    _download_video(yt_downloader)
    yt_video.save()
    return yt_video
        
def _video_in_db(url: str) -> Optional[YouTubeVideo]:
    return YouTubeVideo.objects.filter(url=url).first()

def _get_info(url: str) -> pytube.YouTube:
    yt_downloader = pytube.YouTube(url, on_complete_callback=_download_completed, on_progress_callback=_download_progress)
    logger.info(yt_downloader)
    return yt_downloader

    
def _create_video_obj(url: str, yt_downloader: pytube.YouTube):
    return YouTubeVideo(name=yt_downloader.title, description=yt_downloader.description, url=url, length=yt_downloader.length, date_added=timezone.now(), thumbnail=yt_downloader.thumbnail_url)
      

def _download_video(yt_downloader: pytube.YouTube, download_path: str =config.DOWNLOAD_PATH, skip_existing=True):
    logger.info(f"Downloading video: {yt_downloader.title}")
    file_path = yt_downloader.streams.get_highest_resolution().download(output_path=download_path, skip_existing=skip_existing)
    logger.info(f"Video {yt_downloader.title} saved to {file_path}")
    return yt_downloader.streams.get_highest_resolution().download(output_path=download_path, skip_existing=skip_existing)
    
    
def _download_completed(stream: pytube.Stream, file_path: str) -> str:
    logger.info(f"{stream.title} download finished")
    return file_path

def _download_progress(stream: pytube.Stream, chunk, bytes_remaining):
    logger.info(
        f"{stream.title} progress: {round((1 - (bytes_remaining / stream.filesize)) * 100, 0)}%"
    )