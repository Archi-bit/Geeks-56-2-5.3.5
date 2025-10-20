from django.urls import path
from .views import RegisterView, ConfirmView, LoginView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='user-register'),
    path('confirm/', ConfirmView.as_view(), name='user-confirm'),
    path('login/', LoginView.as_view(), name='user-login'),
]
