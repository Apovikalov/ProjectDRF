from django.core.validators import FileExtensionValidator
from django.db import models

from config import settings


class Course(models.Model):
    name = models.CharField(max_length=30, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='images/', verbose_name='Изображение')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ['name']


class Lesson(models.Model):
    name = models.CharField(max_length=30, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='images/', verbose_name='Изображение')
    video = models.FileField(
        upload_to='videos/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['mp4', 'webm', 'mkv'])]
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons', verbose_name='Курс')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ['name']
