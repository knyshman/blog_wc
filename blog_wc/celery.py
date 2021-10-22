import os

# Из только что установленной библиотеки celery импортируем класс Celery
from celery import Celery

# Указываем где находится модуль django и файл с настройками django (имя_вашего_проекта.settings)
# в свою очередь в файле settings будут лежать все настройки celery.
# Соответственно при указании данной директивы нам не нужно будет при вызове каждого task(функции) прописывать
# эти настройки.
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_wc.settings')

# Создаем объект(экземпляр класса) celery и даем ему имя
app = Celery('blog_wc')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


# app.conf.beat_schedule = {
#     'add_articles': {
#         'task': 'parser.tasks.get_articles',
#         'schedule': crontab(day_of_week=[0, 2, 6]),
#     },
# }
#
# app.conf.beat_schedule = {
#     'send-everyday': {
#         'task': 'blog.tasks.send_mails_to_subscribers',
#         'schedule': crontab(hour=12, minute=30),
#     },
# }