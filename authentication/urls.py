from django.urls import path
from .views import RegistrationView, LoginView, EmailVerificationView, LogoutView

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='users'),
    path('login/', LoginView.as_view(), name='login'),
    path('verify-email/', EmailVerificationView.as_view(), name='verify'),
    path('logout/', LogoutView.as_view(), name='logout')
]
