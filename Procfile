web: gunicorn blog_wc.wsgi --log-file -
worker: celery -A blog_wc worker
web: celery -A blog_wc beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler

