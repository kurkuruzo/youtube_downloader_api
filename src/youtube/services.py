import json
import logging
from turtle import title
import pytube
from typing import Optional
from django.utils import timezone
from yt_dlp import YoutubeDL
from .models import YouTubeVideo
from .tasks import download_video


class YouTubeError(Exception):
    pass


logger = logging.getLogger(__name__)
logger.addHandler(logging.FileHandler('django_services.log', mode='a'))

def add_video(url: str, chat_id: Optional[int] = None, message_id: Optional[int] = None):
    logger.info(f"STARTING ASYNC TASK FOR VIDEO {url}")
    video_in_db = _video_in_db(url)
    logger.info(f"{video_in_db=}")
    # yt_downloader = _get_downloader(url=url)
    with YoutubeDL() as ydl:
        if video_in_db:
            if not video_in_db.filesize_OK:
                video = video_in_db
            else:
                return (video_in_db.id, "")
        else:
            video = _create_video_obj(url=url, downloader=ydl)
        download_status = _download_video(url=url, downloader=ydl, video=video, chat_id=chat_id, message_id=message_id)
    return download_status

def _download_video(url: str, downloader: YoutubeDL, video: YouTubeVideo, chat_id: int, message_id: int):
    download_task = download_video.delay(downloader, video, chat_id, message_id)
    logger.info(f"{download_task=}")
    return (video.id, download_task.id)

def _create_video_obj(url: str, downloader: YoutubeDL) -> YouTubeVideo:
    try:
        info = downloader.extract_info(url, download=False)
        sanitized_info = downloader.sanitize_info(info)
    except Exception as e:
        raise YouTubeError("Возникла ошибка при получении информации о видео. Объект для скачивания не создан.")
    if not sanitized_info:
        raise YouTubeError("Не удалось получить информацию о видео. Объект для скачивания не создан.")
    video_obj = YouTubeVideo.objects.create(
        name=sanitized_info.get("title"),
        description=sanitized_info.get("description"),
        url=url,
        length=sanitized_info.get("duration"),
        date_added=timezone.now(),
        thumbnail=sanitized_info.get("thumbnail"),
        path=downloader.prepare_filename(sanitized_info)
    )
    logger.info(f"{video_obj.__dict__=}")
    return video_obj


def _video_in_db(url: str) -> Optional[YouTubeVideo]:
    logger.info(
        f"Found video with url={url}, video object={YouTubeVideo.objects.filter(url=url).first()}"
    )
    return YouTubeVideo.objects.filter(url=url).first()


# def _get_downloader(url: str) -> :
    # yt_downloader = pytube.YouTube(
    #     url,
    #     on_complete_callback=_download_completed,
    #     on_progress_callback=_download_progress,
    # )
    # logger.info(yt_downloader)
    # return yt_downloader
    



def _download_completed(stream: pytube.Stream, file_path: str = None) -> None:
    logger.info(f"{stream.title} download finished")


def _download_progress(stream: pytube.Stream, chunk, bytes_remaining) -> None:
    logger.info(
        f"{stream.title} progress: {round((1 - (bytes_remaining / stream.filesize)) * 100, 0)}%"
    )
