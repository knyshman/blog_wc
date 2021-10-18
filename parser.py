import json

import requests
from bs4 import BeautifulSoup as BS
from random import randint


# headers = [
#     {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
#         'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
#     {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
#         'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
#     {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:53.0) Gecko/20100101 Firefox/53.0',
#         'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
#     ]
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
url = 'https://itc.ua/news/'

def get_global_html(url):
    html = []
    html.append(requests.get(url, headers=headers).text)
    page_number = 2
    next_url = f'{url}page/{page_number}/'
    while requests.get(next_url, headers=headers).status_code != 404:
        html.append(requests.get(next_url, headers=headers).text)
        page_number += 1
        if page_number == 3:
            break
    return html

def get_urls():
    response_list = get_global_html(url)
    links_list = []
    for html in response_list:
        soup = BS(html, 'html.parser')
        links_list.extend(soup.find_all('h2')[:-1])
    urls = []
    for link in links_list:
        urls.append(link.a.get('href'))
    return urls

def get_content():
    urls = get_urls()
    articles = []
    for url in urls:
        response = requests.get(url, headers=headers).content
        soup = BS(response, 'html.parser')
        main = soup.find('div', class_='entry-content clearfix')
        content = main.findAll('p')
        text = []
        for el in content:
             text.append(el.text)
        images = []
        for im in soup.findAll('img'):
            images.append(im.get('src'))
        author = soup.find('span', class_='vcard author part hidden-xs')
        category = soup.find('span', class_='cat part text-uppercase').text
        articles.append(
        {
            'category': category,
            'date_create': soup.find('time', class_='published').get('datetime'),
            'title': soup.find('div', class_='h1 text-uppercase entry-title').text,
            'preview_image': content[0].find('img').get('src'),
            'slug': str(url).replace(f'https://www.itc.ua/', '')[:-5],
            'short_description': content[1].text,
            'content': ('\n').join(text[2:]),
            'author': author.find('a', rel='author follow').text,
            'images': images
            # 'author_image': soup.find('div', class_='author').get('src')

        }
        )
    return articles


def save_json():
    articles = get_content()
    with open("articles.json", "w", encoding='utf-8') as file:
        json.dump(articles, file, ensure_ascii=False)
save_json()
