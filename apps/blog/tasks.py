from .utils import send
from blog_wc.celery import app


@app.task
def send_mails_to_subscribers(subject, html, from_email, to_email):
    send(subject, html, from_email, to_email)
    print('something')
