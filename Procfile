web: gunicorn blog_wc.wsgi --log-file -
worker1: celery -A blog_wc beat -l info
worker2: celery -A blog_wc worker -l info
