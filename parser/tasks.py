from parser.run_parcer import save_articles, save_sport_articles
from parser.parser import save_itc_json
from parser.sport_parcer import save_sport_json
from blog_wc.celery import app


@app.task
def get_json():
    save_sport_json()
    save_sport_articles()


@app.task
def get_articles():
    save_itc_json()
    save_articles()
    save_sport_json()
    save_sport_articles()