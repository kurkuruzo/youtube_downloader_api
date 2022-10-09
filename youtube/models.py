import uuid
from django.db import models
from pathlib import Path

# Create your models here.
class YouTubeVideo(models.Model):
    name = models.CharField(max_length=500)
    description = models.TextField(max_length=3500, null=True, blank=True)
    url = models.CharField(max_length=1500)
    path = models.CharField(max_length=1500, null=True, blank=True)
    length = models.IntegerField(null=True, blank=True)
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
    def is_downloaded(self):
        return Path(self.path).is_file()
    
    def __str__(self):
        return f"<Video: {self.name}>"