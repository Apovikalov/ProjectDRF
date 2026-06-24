from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.core.mail import send_mail
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from rest_framework import filters, generics, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import Payment, User
from .serializers import PaymentSerializer, UserSerializer


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
