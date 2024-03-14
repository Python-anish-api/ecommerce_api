from django.urls import path
from userauths import views as userauth_views
from rest_framework_simplejwt.views import TokenRefreshView
from store import views as store_views

urlpatterns = [
    path('user/token/', userauth_views.MyTokenObtainPairView.as_view()),
    path('user/token/refresh/', TokenRefreshView.as_view()),
    path('user/register/', userauth_views.RegisterView.as_view()),
    path('user/password-reset/<email>/', userauth_views.PasswordResetEmailVerify.as_view(), name='password_reset'),
    path('user/password-change/', userauth_views.PasswordChangeView.as_view(), name='password_reset'),
    
    # store models
    path('categories/', store_views.CategoryListApiView.as_view(), name='categories'),
    path('products/', store_views.ProductListApiView.as_view(), name='products'),
    path('product-detail/<slug>/', store_views.ProductDetailApiView.as_view(), name='product-detail'),
    
    
    path('cart-view/', store_views.CartApiView.as_view()),
    path('cart-list/<str:cart_id>/', store_views.CartListView.as_view(), name='cart-list'),
    path('cart-list/<str:cart_id>/<int:user_id>/', store_views.CartListView.as_view()),
    path('cart-detail/<str:cart_id>/', store_views.CartDetailView.as_view()),
    path('cart-detail/<str:cart_id>/<int:user_id>/', store_views.CartDetailView.as_view()),
    
    path('cart-delete/<str:cart_id>/<int:item_id>/', store_views.CartItemDeleteApiView.as_view()),
    path('cart-delete/<str:cart_id>/<int:item_id>/<int:user_id>/', store_views.CartItemDeleteApiView.as_view(), name='cart-delete'),
    
    
    path('create-order/', store_views.CreateOrderView.as_view(), name='cart-delete'),
    path('checkout/<order_oid>/', store_views.CheckoutView.as_view(), name='checkout'),

    
    path('coupon/', store_views.CouponApiView.as_view()),
    path('stripe-payment/<order_oid>/', store_views.StripeCheckoutView.as_view()),

    
]