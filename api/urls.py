from django.urls import path
from userauths import views as userauth_views



urlpatterns = [
    path('user/token/', userauth_views.MyTokenObtainPairView.as_view()),
    path('user/register/', userauth_views.RegisterView.as_view()),
]