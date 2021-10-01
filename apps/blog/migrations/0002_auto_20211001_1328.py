# Generated by Django 3.2.7 on 2021-10-01 13:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='draft',
            field=models.BooleanField(default=True, null=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='article_author', to='blog.author', verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='article',
            name='author_en',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='article_author', to='blog.author', verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='article',
            name='author_ru',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='article_author', to='blog.author', verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='article',
            name='author_uk',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='article_author', to='blog.author', verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='author',
            name='name',
            field=models.CharField(max_length=100, unique=True, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='author',
            name='name_en',
            field=models.CharField(max_length=100, null=True, unique=True, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='author',
            name='name_ru',
            field=models.CharField(max_length=100, null=True, unique=True, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='author',
            name='name_uk',
            field=models.CharField(max_length=100, null=True, unique=True, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=200, unique=True, verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name_en',
            field=models.CharField(max_length=200, null=True, unique=True, verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name_ru',
            field=models.CharField(max_length=200, null=True, unique=True, verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name_uk',
            field=models.CharField(max_length=200, null=True, unique=True, verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_set', related_query_name='comments_set', to='blog.article'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(blank=True, max_length=200, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='comment',
            name='rating',
            field=models.CharField(blank=True, choices=[('1', 'very bad'), ('2', 'bad'), ('3', 'good'), ('4', 'very good'), ('5', 'excellent')], max_length=10, null=True, verbose_name='Рейтинг'),
        ),
        migrations.AlterField(
            model_name='semicategory',
            name='name',
            field=models.CharField(max_length=250, verbose_name='Название'),
        ),
    ]