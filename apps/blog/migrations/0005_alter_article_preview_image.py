# Generated by Django 3.2.8 on 2021-10-12 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_alter_like_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='preview_image',
            field=models.ImageField(blank=True, default='default.jpg', upload_to=''),
        ),
    ]
