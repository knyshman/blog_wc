import json
import uuid
from urllib.request import urlretrieve
from django.contrib.auth import get_user_model
from django.db import DatabaseError
from django.conf import settings
from apps.blog.models import Category, Article, Image


User = get_user_model()

categories = [category.name for category in Category.objects.all()]


def save_articles():
    with open('articles.json') as json_file:
        data = json.load(json_file)
        for art in data:
            if art['category'] not in categories:
                try:
                    c = Category(name=art['category'], depth=1, path=f'{uuid.uuid4()}')
                    c.save()
                    categories.append(c.name)
                except DatabaseError:
                    c = Category.objects.filter(name=art['category']).first()
                finally:
                    category = Category.objects.filter(name='Новости').first()
            else:
                c = Category.objects.filter(name=art['category']).first()
            current_article = Article.objects.filter(title=art['title'])
            if not current_article:
                print('new Article')
                try:
                    image_name = f'{str(uuid.uuid4())}.jpg'
                    image_path = f'{settings.MEDIA_ROOT}/{image_name}'
                    preview_image = urlretrieve(art['preview_image'], image_path)

                    article = Article(title=art['title'],
                                      slug=art['slug'],
                                      author=User.objects.first(),
                                      short_description=art['short_description'],
                                      content=art['content'],
                                      category=c if c else category,
                                      preview_image=image_name

                                      )

                    article.save()
                    print('ok')
                    images = art['images']
                    if images:
                        try:
                            for image in images[1:]:
                                image_name = f'{str(uuid.uuid4())}.jpg'
                                image_path = f'{settings.MEDIA_ROOT}/{image_name}'
                                image_file = urlretrieve(image, image_path)
                                new_image = Image(article=article, image=image_name, alt=image_name)
                                new_image.save()
                        except ValueError:
                            print('image saving error')
                except (DatabaseError, UnicodeEncodeError, OSError):
                    print('not save')
            else:
                continue


def save_sport_articles():
    with open('sport.json') as json_file:
        data = json.load(json_file)
        for art in data:
            if art['category'] not in categories:
                try:
                    c = Category(name=art['category'], depth=1, path=f'{uuid.uuid4()}')
                    c.save()
                    categories.append(c.name)
                except DatabaseError:
                    c = Category.objects.filter(name=art['category']).first()
                finally:
                    category = Category.objects.filter(name='Новости').first()
            else:
                c = Category.objects.filter(name=art['category']).first()
            current_article = Article.objects.filter(title=art['title'])
            if not current_article:
                try:
                    image_name = f'{str(uuid.uuid4())}.jpg'
                    image_path = f'{settings.MEDIA_ROOT}/{image_name}'
                    preview_image = urlretrieve(art['preview_image'], image_path)

                    article = Article(title=art['title'],
                                      slug=art['slug'],
                                      author=User.objects.first(),
                                      short_description=art['short_description'],
                                      content=art['content'],
                                      category=c if c else category,
                                      preview_image=image_name

                                      )

                    article.save()
                except (DatabaseError, UnicodeEncodeError, OSError):
                    continue
            else:
                continue
