from django.db import models
from datetime import date, datetime
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from django import forms
from stdimage.models import StdImageField

def upload_location(instance, filename):
    return "%s/%s" %(instance.id, filename)


class Profile(models.Model):
    SEX = [
        ("Женский","Женский"),
        ("Мужской","Мужской")
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='', default='')
    first_name = models.CharField(verbose_name='Имя', max_length=30, default='')
    last_name = models.CharField(verbose_name='Фамилия', max_length=30, default='')
    avatar = models.ImageField(upload_to='upload_location', verbose_name="Аватар", default='')
    city = models.CharField(verbose_name='Город', max_length=20, default='')
    email = models.EmailField(max_length=30, default='')
    sex = models.CharField(verbose_name='Пол', max_length=7,
        choices=SEX, default='')
    contacts = models.TextField(verbose_name='Контакты', max_length=150, blank=True, null=True, default='')
    biography = models.TextField(verbose_name='Биография', max_length=400, blank=True, null=True, default='')
    other_info = models.TextField(verbose_name='Прочая информация', max_length=400, blank=True, null=True, default='')
    created = models.DateTimeField(verbose_name='Создан', auto_now_add=True, blank=True, null=True)

    class Meta:
        ordering = ["-created"]

    def get_absolute_url(self):
        return reverse('profile-detail', args=[str(self.id)])

    def __str__(self):
        return self.user.username

from django.utils.html import escape

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=50)
    body = RichTextUploadingField()
    logo = StdImageField(upload_to=upload_location,variations={'thumbnail': {"width": 150, "height": 150, "crop": True}}, default='')
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    moderation = models.BooleanField(default=False)
    post_date = models.DateField(default=date.today)

    class Meta:
        ordering = ["-post_date"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    description = RichTextUploadingField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    comment_date = models.DateTimeField(auto_now_add=True, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-comment_date"]

    def __str__(self):
        return "{}".format(self.description)
