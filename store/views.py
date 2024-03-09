from django.shortcuts import render

from store.models import Cart, Product, Category, Tax
from store.serializers import CartSerializer, CategorySerializer, ProductSerializer
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from decimal import Decimal
from rest_framework.response import Response
from rest_framework import status

from userauths.models import User
# Create your views here.


class CategoryListApiView(generics.ListAPIView):
    queryset = Category.objects.all()
    permission_classes = [AllowAny, ]
    serializer_class = CategorySerializer
    
    
class ProductListApiView(generics.ListAPIView):
    queryset = Product.objects.all()
    permission_classes = [AllowAny, ]
    serializer_class = ProductSerializer
    

class ProductDetailApiView(generics.RetrieveAPIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny, ]
    
    def get_object(self):
        slug = self.kwargs.get('slug')
        return Product.objects.get(slug=slug)    
    
    

class CartApiView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    queryset = Cart.objects.all()
    permission_classes  = [AllowAny, ]
    
    
    def create(self, request, *args, **kwargs):
        payload = request.data
        product_id = payload['product']
        user_id = payload['user']
        qty = payload['qty']
        price = payload['price']
        shipping_amount = payload['shipping_amount']
        country = payload['country']
        size = payload['size']
        color = payload['color']
        cart_id = payload['cart_id']    
        product = Product.objects.get(id=product_id)
        if user_id != 'undefined':
            user = User.objects.get(id=user_id)
        else:
            user = None
            
        tax = Tax.objects.filter(country=country).first()
        if tax:
            tax_rate = tax.rate / 100
            
        else:
            tax_rate = 0      
        
        cart = Cart.objects.filter(cart_id=cart_id, product=product).first()
        if cart:
            cart.product = product
            cart.user = user
            cart.qty = qty
            cart.price = price
            cart.sub_total = Decimal(price) * int(qty)
            cart.shipping_amount = Decimal(shipping_amount) * int(qty)
            cart.size = size
            cart.tax_fee = int(qty) * Decimal(tax_rate)
            cart.color = color
            cart.country = country
            cart.cart_id = cart_id

            service_fee_percentage =  10 / 100
            cart.service_fee = service_fee_percentage * cart.sub_total
            cart.total = cart.sub_total + cart.shipping_amount + cart.service_fee + cart.tax_fee
            cart.save()
            return Response( {"message": "Cart Created Successfully"}, status=status.HTTP_201_CREATED)
        
        else:
            cart = Cart()
            cart.product = product
            cart.user = user
            cart.qty = qty
            cart.price = price
            cart.sub_total = Decimal(price) * int(qty)
            cart.shipping_amount = Decimal(shipping_amount) * int(qty)
            cart.size = size
            cart.tax_fee = int(qty) * Decimal(tax_rate)
            cart.color = color
            cart.country = country
            cart.cart_id = cart_id
            service_fee_percentage =  20 / 100
            cart.service_fee = service_fee_percentage * cart.sub_total
            cart.total = cart.sub_total + cart.shipping_amount + cart.service_fee + cart.tax_fee
            cart.save()
            return Response( {"message": "Cart Created Successfully"}, status=status.HTTP_201_CREATED)
