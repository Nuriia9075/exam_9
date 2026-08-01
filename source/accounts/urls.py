from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from accounts.views import RegisterView, UserDetailView, UserChangeView, UserPasswordChangeView

app_name = "accounts"

urlpatterns = [
    path('login/', LoginView.as_view(template_name="accounts/login.html"), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('<int:pk>/detail/', UserDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', UserChangeView.as_view(), name='edit'),
    path('<int:pk>/password-change/', UserPasswordChangeView.as_view(), name='password-change'),
]