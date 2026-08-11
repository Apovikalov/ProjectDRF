from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

from materials.models import CourseSubscription
from django.conf import settings


@shared_task
def send_email_for_update_course(course_id):
    """
    Отправляем сообщение об обновлении курса
    :param course_id: идентификатор курса
    """
    subs = CourseSubscription.objects.filter(course=course_id, status=True)
    for sub in subs:
        course = sub.course
        user = sub.owner
        send_mail(
            subject=f'{course} обновился',
            message=f'{course} обновился',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False
        )


@shared_task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 3})
def check_and_block_inactive_users(self):
    # Рассчитываем порог: сегодня минус 1 месяц
    cutoff_date = timezone.now() - timedelta(days=30)

    # Используем фильтр для оптимизации: получаем только тех, у кого last_login раньше cutoff
    inactive_users = User.objects.filter(last_login__lt=cutoff_date, is_active=True)

    # Обновляем флаг is_active для каждого найденного пользователя
    for user in inactive_users:
        user.is_active = False
        user.save(update_fields=['is_active'])
