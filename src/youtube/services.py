import json
import logging
# import pytube
from celery.result import AsyncResult
from typing import Optional
from django.utils import timezone
from yt_dlp import YoutubeDL
from .models import YouTubeVideo
from .producer import send_download_confirmation
from .tasks import download_video



class YouTubeError(Exception):
    pass


logger = logging.getLogger(__name__)
logger.addHandler(logging.FileHandler('django_services.log', mode='a'))

def add_video(url: str, chat_id: Optional[int] = None, message_id: Optional[int] = None):
    logger.info(f"STARTING ASYNC TASK FOR VIDEO {url}")
    video_in_db = _video_in_db(url)
    logger.info(f"{video_in_db=}")

    with YoutubeDL() as ydl:
        if video_in_db:
            # if video_in_db.filesize_OK:
            #     return video_in_db
            video = video_in_db
        else:
            video = _create_video_obj(url=url, downloader=ydl)
    #         download_task_id = _download_video(video=video)
    # return download_task_id
    return video


# def download_video(video: YouTubeVideo):
#     download_task: AsyncResult  = download_video.delay(video)
#     logger.info(f"{download_task.id=}")
#     return download_task

def _create_video_obj(url: str, downloader: YoutubeDL) -> YouTubeVideo:
    try:
        info = downloader.extract_info(url, download=False)
        sanitized_info = downloader.sanitize_info(info)
    except Exception:
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
    



# def _download_completed(stream: pytube.Stream, file_path: str = None) -> None:
#     logger.info(f"{stream.title} download finished")


# def _download_progress(stream: pytube.Stream, chunk, bytes_remaining) -> None:
#     logger.info(
#         f"{stream.title} progress: {round((1 - (bytes_remaining / stream.filesize)) * 100, 0)}%"
#     )

def send_successful_download_confirmation(yt_video: YouTubeVideo, chat_id: int, message_id: int):
    try:
        send_download_confirmation(json.dumps({'yt_video_id': str(yt_video.id), "chat_id": chat_id, "message_id": message_id}))
    except Exception:
        logger.exception("Failed to send confirmation")