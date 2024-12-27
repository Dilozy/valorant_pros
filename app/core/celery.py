import os

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')

# Загружаем настройки из Django settings
app.config_from_object('django.conf:settings')

app.conf.broker_url = settings.CELERY_BROKER_URL

# Автоматически находим все задачи
app.autodiscover_tasks()
