from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Course, Lesson


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='E-mail')
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name='Номер телефона')
    avatar = models.ImageField(upload_to='images/', null=True, verbose_name='Аватар')
    city = models.CharField(max_length=30, default=None, null=True, verbose_name='Город')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment', verbose_name='Пользователь')
    pay_date = models.DateField(verbose_name='Дата оплаты')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True, related_name='payment', verbose_name='Курс')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, blank=True, null=True, related_name='payment', verbose_name='Урок')
    pay_sum = models.FloatField(verbose_name='Сумма оплаты')
    payment_way = models.CharField(max_length=30, verbose_name='Способ оплаты')

    def __str__(self):
        return f'{self.user}, {self.pay_date}'

    class Meta:
        verbose_name = 'Платёж'
        verbose_name_plural = 'Платежи'
        ordering = ['pay_date']
