from django.contrib.auth import get_user_model
from django.db import DatabaseError
from django.conf import settings
import json
import uuid
import boto3
import requests
from apps.blog.models import Category, Article, Image


User = get_user_model()

categories = [category.name for category in Category.objects.all() if Category.objects.all()]


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
                try:
                    image_name = f'{str(uuid.uuid4())}.jpg'
                    AWS_S3_CREDS = {
                        "aws_access_key_id": settings.AWS_ACCESS_KEY_ID,
                        "aws_secret_access_key": settings.AWS_SECRET_ACCESS_KEY,
                        "region_name": settings.AWS_S3_REGION_NAME,
                    }
                    resp = requests.get(art['preview_image'])
                    s3 = boto3.resource('s3', **AWS_S3_CREDS)
                    obj = s3.Object(settings.AWS_STORAGE_BUCKET_NAME, f'media/{image_name}')
                    obj.put(Body=resp.content)

                    article = Article(title=art['title'],
                                      slug=art['slug'],
                                      author=User.objects.first(),
                                      short_description=art['short_description'],
                                      content=art['content'],
                                      category=c if c else category,
                                      preview_image=image_name

                                      )

                    article.save()
                    images = art['images']
                    if images:
                        try:
                            for image in images[1:]:
                                resp = requests.get(image)
                                s3 = boto3.resource('s3', **AWS_S3_CREDS)
                                image_name = f'{str(uuid.uuid4())}.jpg'
                                obj = s3.Object(settings.AWS_STORAGE_BUCKET_NAME, f'media/{image_name}')
                                obj.put(Body=resp.content)
                                new_image = Image(article=article, image=image_name, alt=image_name)
                                new_image.save()
                        except ValueError:
                            pass
                except (DatabaseError, UnicodeEncodeError, OSError):
                    pass
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
                    AWS_S3_CREDS = {
                        "aws_access_key_id": settings.AWS_ACCESS_KEY_ID,
                        "aws_secret_access_key": settings.AWS_SECRET_ACCESS_KEY,
                        "region_name": settings.AWS_S3_REGION_NAME,
                    }
                    resp = requests.get(art['preview_image'])
                    s3 = boto3.resource('s3', **AWS_S3_CREDS)
                    obj = s3.Object(settings.AWS_STORAGE_BUCKET_NAME, f'media/{image_name}')
                    obj.put(Body=resp.content)

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
