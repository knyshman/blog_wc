# Generated by Django 3.2.8 on 2021-10-08 12:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='articlerating',
            old_name='author',
            new_name='user',
        ),
    ]