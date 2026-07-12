from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.core.mail import send_mail
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from rest_framework import filters, generics, permissions, response, views, viewsets
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from .models import Payment, Subscription, User
from .serializers import PaymentSerializer, UserSerializer
from .services import create_stripe_product, create_stripe_price, create_stripe_session

from materials.models import Course


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class RegisterView(FormView):
    template_name = 'register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        self.send_welcome_email(user.email)
        return super().form_valid(form)

    def send_welcome_email(self, user_email):
        subject = 'Добро пожаловать в наш сервис'
        message = 'Спасибо, что зарегистрировались в нашем сервисе!'
        from_email = 'your_email@yandex.ru'
        recipient_list = [user_email]
        send_mail(subject, message, from_email, recipient_list)


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['user', 'pay_date']
    ordering_fields = ['pay_date']
    filterset_fields = ['course', 'lesson', 'payment_way']

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        if payment.course is None and payment.lesson is None:
            raise ValidationError("Нужно выбрать курс или урок")
        elif payment.course and payment.lesson:
            raise ValidationError("Нужно выбрать либо курс, либо урок")
        else:
            if payment.course:
                product = create_stripe_product(payment.course)
            else:
                product = create_stripe_product(payment.lesson)
        price = create_stripe_price(stripe_product=product, amount=payment.amount)
        session_id, session_url = create_stripe_session(price)
        payment.session_id = session_id
        payment.link = session_url
        payment.save()


class SubscriptionManagementView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course_id')

        course_item = get_object_or_404(Course, id=course_id)

        subscription, created = Subscription.objects.get_or_create(user=user, course=course_item)
        if not created:
            subscription.delete()
            message = "Подписка удалена"
        else:
            message = "Подписка добавлена"

        return response.Response({"message": message})
