from __future__ import absolute_import

import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_wc.settings')
from django.conf import settings
celery_app = Celery('blog_wc')

celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
CELERY_IMPORTS = ("apps.blog.tasks", )
