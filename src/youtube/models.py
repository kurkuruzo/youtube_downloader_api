import logging
import os
import uuid
from django.db import models
from django.templatetags.static import static
from pathlib import Path

from api.settings import DOWNLOAD_PATH


logger = logging.getLogger(__name__)
# Create your models here.
class YouTubeVideo(models.Model):
    name = models.CharField(max_length=500)
    description = models.TextField(max_length=3500, null=True, blank=True)
    url = models.CharField(max_length=1500, unique=True)
    path = models.CharField(max_length=1500, null=True, blank=True)
    length = models.IntegerField(null=True, blank=True)
    filesize = models.IntegerField(null=True, blank=True)
    date_added = models.DateTimeField()
    # thumbnail = models.ImageField(null=True, blank=True)
    thumbnail = models.URLField(null=True, blank=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    class Meta:
        ordering = ("-date_added",)
        verbose_name = "Видео с YouTube"
        verbose_name_plural = "Видео с YouTube"

    @property
    def local_file_exists(self):
        file_path = (Path(DOWNLOAD_PATH) / self.path).resolve()
        file_exists = file_path.is_file()
        logger.info(f"Video is downloaded = {file_exists}")
        return file_exists

    @property
    def filesize_OK(self):
        file_path = (Path(DOWNLOAD_PATH) / self.path).resolve()
        if Path(file_path).is_file():
            return os.stat(file_path).st_size == self.filesize
        return False

    @property
    def abs_path(self):
        static_file_path = str((Path(DOWNLOAD_PATH) / self.path).resolve())
        logger.info(f"{static_file_path=}")
        return static_file_path

    @property
    def download_url(self):
        return static(f"downloads/{self.path}")

    def __str__(self):
        return f"<Video: {self.name}, {str(self.id)}>"

    @classmethod
    def get_by_id(cls, id: str):
        logger.info(f"{id=}")
        return cls.objects.get(pk=id)

    @classmethod
    def get_by_url(cls, url: str):
        logger.info(f"{url=}")
        return cls.objects.filter(url=url)
