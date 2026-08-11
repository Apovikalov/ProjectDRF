from django.core.management.base import BaseCommand
from users.models import Payment, User
from materials.models import Course, Lesson

class Command(BaseCommand):
    help = 'Add test payments to the database'

    def handle(self, *args, **kwargs):
        user, _ = User.objects.get_or_create(email='admin@mail.ru')
        course, _ = Course.objects.get_or_create(name='Python course')
        lesson, _ = Lesson.objects.get_or_create(name='Print')

        payments = [
            {'user': user, 'pay_date': '2026-5-11', 'course': course, 'pay_sum': 100, 'payment_way': 'Наличные'},
            {'user': user, 'pay_date': '2026-5-12', 'lesson': lesson, 'pay_sum': 130, 'payment_way': 'Счёт'},
        ]
        for payment_data in payments:
            payment, created = Payment.objects.get_or_create(**payment_data)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully added payment: {payment.user}, {payment.pay_date}'))
            else:
                self.stdout.write(
                    self.style.WARNING(f'Payment already exists: {payment.user}, {payment.pay_date}'))
