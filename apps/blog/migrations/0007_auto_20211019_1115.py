# Generated by Django 3.2.8 on 2021-10-19 08:15

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0006_alter_like_article'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='average_rating',
            field=models.FloatField(default=0, verbose_name='Средний рейтинг'),
        ),
        migrations.AlterField(
            model_name='article',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='article',
            name='likes',
            field=models.IntegerField(default=0, verbose_name='Лайки'),
        ),
        migrations.AlterField(
            model_name='article',
            name='preview_image',
            field=models.ImageField(blank=True, default='default.jpg', upload_to='', verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='article',
            name='update_date',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата изменения'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_set', related_query_name='comments_set', to='blog.article', verbose_name='Статья'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='пользователь'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='comment',
            field=ckeditor.fields.RichTextField(verbose_name='Комментарий'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='дата создания'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='is_published',
            field=models.BooleanField(default=True, null=True, verbose_name='опубликовано'),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='')),
                ('alt', models.CharField(max_length=200)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.article')),
            ],
        ),
    ]