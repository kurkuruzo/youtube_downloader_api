from .celery import app as celery_app
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d:%m:%Y %I:%M:%S %p', level=logging.INFO)

__all__ = ('celery_app',)