from __future__ import absolute_import, unicode_literals
import os
from datetime import timedelta

from celery import Celery

# Установка переменной окружения для настроек проекта
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Создание экземпляра объекта Celery
app = Celery('config',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/1',
    include=['materials.tasks']
)

# Загрузка настроек из файла Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматическое обнаружение и регистрация задач из файлов tasks.py в приложениях Django
app.autodiscover_tasks()

# Важные настройки для корректного расписания
app.conf.update(
    timezone='UTC',
    enable_utc=True,
)

app.conf.beat_schedule = {
    'check_inactive_users': {
        'task': 'myproject.tasks.check_and_block_inactive_users',
        'schedule': timedelta(days=1),  # Раз в день
    },
}
