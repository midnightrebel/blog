# Generated by Django 4.0.3 on 2022-03-22 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_remove_comment_body_remove_comment_slug_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='slug',
            field=models.SlugField(default='com', verbose_name='URL-Адрес'),
        ),
    ]
