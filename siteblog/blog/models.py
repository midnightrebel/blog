from datetime import timezone

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from authentication.models import User
from django.db.models import Sum
# Create your models here.
from django.urls import reverse


class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(max_length=50, verbose_name='URL-Адрес', unique=True)

    def get_absolute_url(self):
        return reverse('category', kwargs={"slug": self.slug})

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']



class Tags(models.Model):
    title = models.CharField(max_length=50, verbose_name='Заголовок тэга')
    slug = models.SlugField(max_length=50, verbose_name='URL-Адрес', unique=True)

    def get_absolute_url(self):
        return reverse('tag', kwargs={"slug": self.slug})

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        ordering = ['title']


class Blog(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок блога')
    desc = models.TextField(blank=True, verbose_name="Описание блога")
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания блога')
    updatedAt = models.DateTimeField(auto_now=True, verbose_name='Дата последней публикации')
    username = models.ManyToManyField(User, blank=True, related_name='users')
    owner = models.CharField(max_length=150)
    slug = models.SlugField(max_length=50, verbose_name='URL-Адрес', unique=True)

    def get_absolute_url(self):
        return reverse('blog', kwargs={"slug": self.slug})

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'
        ordering = ['title']



class LikeDislikeManager(models.Manager):
    use_for_related_fields = True

    def likes(self):
        # Забираем queryset с записями больше 0
        return self.get_queryset().filter(vote__gt=0)

    def dislikes(self):
        # Забираем queryset с записями меньше 0
        return self.get_queryset().filter(vote__lt=0)

    def sum_rating(self):
        # Забираем суммарный рейтинг
        return self.get_queryset().aggregate(Sum('vote')).get('vote__sum') or 0


class LikeDislike(models.Model):
    LIKE = 1
    DISLIKE = -1

    VOTES = (
        (DISLIKE, 'Не нравится'),
        (LIKE, 'Нравится')
    )

    vote = models.SmallIntegerField(verbose_name=("Голос"), choices=VOTES)
    user = models.ForeignKey(User, verbose_name="Пользователь",on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    objects = LikeDislikeManager()



class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок поста')
    username = models.CharField(max_length=255, verbose_name='Автор поста', blank=True)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    slug = models.SlugField(max_length=50, verbose_name='URL-Адрес', unique=True)
    сontent = models.TextField(blank=True)
    votes = GenericRelation(LikeDislike, related_query_name='articles')
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания публикации')
    updatedAt = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="posts")
    isPublished = models.BooleanField(default=True, verbose_name='Опубликовано')
    views = models.IntegerField(default=0, verbose_name='Количество просмотров')
    tags = models.ManyToManyField(Tags, blank=True, related_name='posts')

    def articles(self):
        return self.get_queryset().filter(content_type__model='article').order_by('-articles_pub_date')

    def get_absolute_url(self):
        return reverse('post', kwargs={"slug": self.slug})

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['createdAt']


class Comment(models.Model):
    authorComment = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='Автор комментария:',blank=True)
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    body = models.TextField(blank=True)
    slug = models.SlugField(max_length=50, verbose_name='URL-Адрес', default="com")
    votes = GenericRelation(LikeDislike, related_query_name='comments')

    def comments(self):
        return self.get_queryset().filter(content_type_model = 'comment').order_by('-comments')

    def get_absolute_url(self):
        return reverse('comment', kwargs={"slug": self.slug})


    class Meta:
        verbose_name = 'Коментарий'
        verbose_name_plural = 'Коментарии'
        ordering = ['createdAt']
