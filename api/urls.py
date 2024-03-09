from django.urls import path
from userauths import views as userauth_views
from rest_framework_simplejwt.views import TokenRefreshView
from store import views as category_views

urlpatterns = [
    path('user/token/', userauth_views.MyTokenObtainPairView.as_view()),
    path('user/token/refresh/', TokenRefreshView.as_view()),
    path('user/register/', userauth_views.RegisterView.as_view()),
    path('user/password-reset/<email>/', userauth_views.PasswordResetEmailVerify.as_view(), name='password_reset'),
    path('user/password-change/', userauth_views.PasswordChangeView.as_view(), name='password_reset'),
    
    # store models
    path('categories/', category_views.CategoryListApiView.as_view(), name='categories'),
    path('products/', category_views.ProductListApiView.as_view(), name='products'),
    path('product-detail/<slug>/', category_views.ProductDetailApiView.as_view(), name='product-detail'),

]