from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import PaymentListAPIView, RegisterView, SubscriptionManagementView, UserViewSet
from users.apps import UsersConfig
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = UsersConfig.name


router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('payments/', PaymentListAPIView.as_view(), name='payments'),
    path('register/', RegisterView.as_view(), name='register'),
    path('subscriptions/', SubscriptionManagementView.as_view(), name='subscriptions'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + router.urls
