# Generated by Django 4.0.3 on 2022-03-14 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_alter_blog_options_alter_category_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='photo',
            field=models.ImageField(blank=True, upload_to='photos/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.CharField(blank=True, max_length=255, verbose_name='Автор поста'),
        ),
    ]
