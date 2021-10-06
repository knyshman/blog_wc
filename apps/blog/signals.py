from django.db.models import Avg
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import ArticleRating


@receiver(pre_save, sender=ArticleRating)
def save_rating(sender, instance, **kwargs):
    if ArticleRating.objects.filter(user=instance.user, article=instance.article):
        ArticleRating.objects.filter(user=instance.user, article=instance.article).delete()


@receiver(post_save, sender=ArticleRating)
def update_rating(sender, instance, **kwargs):
    parent = instance.article
    all_grades = ArticleRating.objects.filter(article=parent)
    if all_grades:
        total_rating = 0
        for grade in all_grades:
            total_rating += grade.rating
        parent.average_rating = round((parent.rating_set.aggregate(avg_rating=Avg('rating'))['avg_rating']), 2)
        parent.save()
    else:
        parent.average_rating = 0
