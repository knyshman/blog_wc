import os

# Из только что установленной библиотеки celery импортируем класс Celery
from celery import Celery

# Указываем где находится модуль django и файл с настройками django (имя_вашего_проекта.settings)
# в свою очередь в файле settings будут лежать все настройки celery.
# Соответственно при указании данной директивы нам не нужно будет при вызове каждого task(функции) прописывать
# эти настройки.
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_wc.settings')

# Создаем объект(экземпляр класса) celery и даем ему имя
celery_app = Celery('blog_wc')

celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks()

celery_app.conf.beat_schedule = {
    'add_articles': {
        'task': 'blog.tasks.get_articles',
        'schedule': crontab(hour=10, minute=45),
    },

    'send-everyday': {
            'task': 'blog.tasks.send_mails_to_subscribers',
            'schedule': crontab(hour=10, minute=45),
            'args': ('subject', 'html', 'from_email', 'users')
        },
    }




