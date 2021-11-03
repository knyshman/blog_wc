from apps.blog.utils import send
from blog_wc.celery import celery_app


@celery_app.task(name='send_mails_to_subscribers')
def send_mails_to_subscribers(subject, html, from_email, to_email):
    send(subject, html, from_email, to_email)


from apps.blog.parser.run_parcer import save_articles, save_sport_articles
from apps.blog.parser.parser import save_itc_json
from apps.blog.parser.sport_parcer import save_sport_json
from apps.blog.parser import saving_errors


@celery_app.task(name='saving_errors')
def search_errors():
    print('start')
    saving_errors.save_articles()


@celery_app.task(name='get_articles')
def get_articles():
    save_itc_json()
    save_articles()
    save_sport_json()
    save_sport_articles()
