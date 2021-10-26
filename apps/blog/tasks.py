from apps.blog.utils import send
from blog_wc.celery import celery_app


@celery_app.task
def send_mails_to_subscribers(subject, html, from_email, to_email):
    send(subject, html, from_email, to_email)


from apps.blog.parser.run_parcer import save_articles, save_sport_articles
from apps.blog.parser.parser import save_itc_json
from apps.blog.parser.sport_parcer import save_sport_json


@celery_app.task
def get_articles():
    print('begin')
    save_itc_json()
    print('save_itc_json')
    save_articles()
    print('save_articles')
    save_sport_json()
    print('save_sport_json')
    save_sport_articles()
    print('end')