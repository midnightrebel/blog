# Generated by Django 4.0.3 on 2022-04-07 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_alter_user_options_user_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='slug',
            field=models.SlugField(default='username', unique=True, verbose_name='URL-Адрес'),
        ),
    ]
