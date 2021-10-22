from django.contrib.admin import site
from django.db.models import Avg
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from .models import ArticleRating, Like, Article
from .tasks import send_mails_to_subscribers
from ..accounts.models import MyUser


@receiver(pre_save, sender=ArticleRating)
def save_rating(sender, instance, **kwargs):
    if ArticleRating.objects.filter(user=instance.user, article=instance.article):
        ArticleRating.objects.filter(user=instance.user, article=instance.article).delete()


@receiver(post_save, sender=ArticleRating)
def update_rating(sender, instance, **kwargs):
    parent = instance.article
    all_grades = ArticleRating.objects.filter(article=parent).select_related('article')
    if all_grades:
        total_rating = 0
        for grade in all_grades:
            total_rating += grade.rating
        parent.average_rating = round((parent.rating_set.aggregate(avg_rating=Avg('rating'))['avg_rating']), 2)
        parent.save()
    else:
        parent.average_rating = 0


@receiver(pre_save, sender=Like)
def save_like(sender, instance, **kwargs):
    if Like.objects.filter(user=instance.user, article=instance.article, like=True).select_related('article', 'user'):
        Like.objects.filter(user=instance.user, article=instance.article, like=True).delete()
        instance.like = False


@receiver(post_save, sender=Like)
def update_likes(sender, instance, **kwargs):
    parent = instance.article
    all_likes = Like.objects.filter(article=parent, like=True).select_related('article')
    parent.likes = all_likes.count()
    parent.save()

#
# from blog_wc.settings import (
#
#     DEFAULT_FROM_EMAIL
# )
# from_email = DEFAULT_FROM_EMAIL
from_email = 'from@example.com'

@receiver(post_save, sender=Article)
def send_mails(sender, instance, **kwargs):
    author = instance.author
    subscribers = MyUser.objects.filter(subscribes__exact=author)
    subject = _('Автором из числа Ваших подписок была опубликована новая статья')
    users = [user.email for user in subscribers]
    html = render_to_string('accounts/email/email_for_subscriber.html', {'object': instance})
    send_mails_to_subscribers.delay(subject, html, from_email, users)
