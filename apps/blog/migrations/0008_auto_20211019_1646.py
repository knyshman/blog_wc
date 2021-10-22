# Generated by Django 3.2.8 on 2021-10-19 13:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20211019_1115'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ['create_date'], 'verbose_name': 'Статья', 'verbose_name_plural': 'Статьи'},
        ),
        migrations.AlterModelOptions(
            name='image',
            options={'ordering': ['alt'], 'verbose_name': 'Изображение', 'verbose_name_plural': 'Изображения'},
        ),
        migrations.AlterField(
            model_name='article',
            name='preview_image',
            field=models.ImageField(blank=True, default='default.jpg', upload_to='', verbose_name='Изображение превью'),
        ),
        migrations.AlterField(
            model_name='image',
            name='article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.article', verbose_name='статья'),
        ),
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to='media', verbose_name='изображение'),
        ),
    ]