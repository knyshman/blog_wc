import json
import re

import requests
from bs4 import BeautifulSoup as BS
from random import randint


__all__ = ('get_itc_content', "save_itc_json")

from apps.blog.models import Article

headers = [
    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:53.0) Gecko/20100101 Firefox/53.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
    ]
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
#         'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
url = 'https://itc.ua/news/'

ARTICLES = [article.title for article in Article.objects.all()]


def get_global_html(url):
    html = []
    html.append(requests.get(url, headers=headers[randint(0, 2)]).text)
    page_number = 2
    next_url = f'{url}page/{page_number}/'
    while requests.get(next_url, headers=headers[randint(0, 2)]).status_code != 404:
        response = requests.get(next_url, headers=headers[randint(0, 2)]).text
        soup = BS(response, 'lxml')
        title = soup.find('h2').text
        if not title in ARTICLES:
            html.append(response)
            page_number += 1
        else:
            break
        if page_number == 3:
            break
    return html


def get_urls():
    response_list = get_global_html(url)
    links_list = []
    for html in response_list:
        soup = BS(html, 'lxml')
        links_list.extend(soup.find_all('h2')[:-1])
    urls = []
    for link in links_list:
        urls.append(link.find('a').get('href'))
    return urls


def get_itc_content():
    urls = get_urls()
    articles = []
    for url in urls:
        response = requests.get(url, headers=headers[randint(0, 2)]).content
        soup = BS(response, 'lxml')
        main = soup.find('div', class_='entry-content clearfix')
        if main:
            content_ = main.findAll('p')
            text = []
            for el in content_:
                 text.append(el.text)
            images = []
            image_list = soup.findAll('img')[:-2]
            for im in image_list:
                images.append(im.get('src'))
            author = soup.find('span', class_='vcard author part hidden-xs')
            category = soup.find('span', class_='cat part text-uppercase').text
            splitted_url = str(url).split('/')
            slug = re.sub('[!@#&%?/$]', '', splitted_url[-2])
            articles.append(
            {
                'category': category.strip(),
                'title': soup.find('div', class_='h1 text-uppercase entry-title').text,
                'preview_image': content_[0].find('img').get('src'),
                'slug': slug,
                'category_slug': splitted_url[-3],
                'short_description': content_[1].text,
                'content': ('\n').join(text[2:]),
                'images': images[1:]

            }
            )
    return articles


def save_itc_json():
    articles = get_itc_content()
    with open("articles.json", "w", encoding='utf-8') as file:
        json.dump(articles, file, ensure_ascii=False, indent=4)