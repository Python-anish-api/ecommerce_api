from django.urls import path
from userauths import views as userauth_views
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('user/token/', userauth_views.MyTokenObtainPairView.as_view()),
    path('user/token/refresh/', TokenRefreshView.as_view()),
    path('user/register/', userauth_views.RegisterView.as_view()),
    path('user/password-reset/<email>/', userauth_views.PasswordResetEmailVerify.as_view(), name='password_reset'),
    path('user/password-change/', userauth_views.PasswordChangeView.as_view(), name='password_reset'),

]