import os

# Из только что установленной библиотеки celery импортируем класс Celery
from celery import Celery

# Указываем где находится модуль django и файл с настройками django (имя_вашего_проекта.settings)
# в свою очередь в файле settings будут лежать все настройки celery.
# Соответственно при указании данной директивы нам не нужно будет при вызове каждого task(функции) прописывать
# эти настройки.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_wc.settings')

# Создаем объект(экземпляр класса) celery и даем ему имя
app = Celery('blog_wc')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()