# Generated by Django 3.2.8 on 2021-10-11 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_alter_article_preview_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='like',
            field=models.BooleanField(default=True),
        ),
    ]