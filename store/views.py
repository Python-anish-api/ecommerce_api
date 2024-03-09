from django.shortcuts import get_object_or_404, render

from store.models import Cart, CartOrder, CartOrderItem, Coupon, Product, Category, Tax
from store.serializers import CartOrderSerializer, CartSerializer, CategorySerializer, ProductSerializer
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


class CartListView(generics.ListAPIView):
    serializer_class = CartSerializer
    permission_classes = ['AllowAny',]
    queryset = Cart.objects.all()
    
    def get_queryset(self):
        cart_id = self.kwargs['cart_id']
        user_id = self.kwargs['user_id']
        
        if user_id is not None:
            user = User.objects.get(id=user_id)
            return Cart.objects.filter(user=user, cart_id=cart_id)
        else:
            return Cart.objects.filter(cart_id=cart_id)
        

    
class CartDetailView(generics.RetrieveAPIView):
    # Define the serializer class for the view
    serializer_class = CartSerializer
    # Specify the lookup field for retrieving objects using 'cart_id'
    lookup_field = 'cart_id'

    # Add a permission class for the view
    permission_classes = (AllowAny,)


    def get_queryset(self):
        # Get 'cart_id' and 'user_id' from the URL kwargs
        cart_id = self.kwargs['cart_id']
        user_id = self.kwargs.get('user_id')  # Use get() to handle cases where 'user_id' is not present

        if user_id is not None:
            # If 'user_id' is provided, filter the queryset by both 'cart_id' and 'user_id'
            user = User.objects.get(id=user_id)
            queryset = Cart.objects.filter(cart_id=cart_id, user=user)
        else:
            # If 'user_id' is not provided, filter the queryset by 'cart_id' only
            queryset = Cart.objects.filter(cart_id=cart_id)

        return queryset

    def get(self, request, *args, **kwargs):
        # Get the queryset of cart items based on 'cart_id' and 'user_id' (if provided)
        queryset = self.get_queryset()

        # Initialize sums for various cart item attributes
        total_shipping = 0.0
        total_tax = 0.0
        total_service_fee = 0.0
        total_sub_total = 0.0
        total_total = 0.0

        # Iterate over the queryset of cart items to calculate cumulative sums
        for cart_item in queryset:
            # Calculate the cumulative shipping, tax, service_fee, and total values
            total_shipping += float(self.calculate_shipping(cart_item))
            total_tax += float(self.calculate_tax(cart_item))
            total_service_fee += float(self.calculate_service_fee(cart_item))
            total_sub_total += float(self.calculate_sub_total(cart_item))
            total_total += round(float(self.calculate_total(cart_item)), 2)

        # Create a data dictionary to store the cumulative values
        data = {
            'shipping': round(total_shipping, 2),
            'tax': total_tax,
            'service_fee': total_service_fee,
            'sub_total': total_sub_total,
            'total': total_total,
        }

        # Return the data in the response
        return Response(data)

    def calculate_shipping(self, cart_item):
        # Implement your shipping calculation logic here for a single cart item
        # Example: Calculate based on weight, destination, etc.
        return cart_item.shipping_amount

    def calculate_tax(self, cart_item):
        # Implement your tax calculation logic here for a single cart item
        # Example: Calculate based on tax rate, product type, etc.
        return cart_item.tax_fee

    def calculate_service_fee(self, cart_item):
        # Implement your service fee calculation logic here for a single cart item
        # Example: Calculate based on service type, cart total, etc.
        return cart_item.service_fee

    def calculate_sub_total(self, cart_item):
        # Implement your service fee calculation logic here for a single cart item
        # Example: Calculate based on service type, cart total, etc.
        return cart_item.sub_total

    def calculate_total(self, cart_item):
        # Implement your total calculation logic here for a single cart item
        # Example: Sum of sub_total, shipping, tax, and service_fee
        return cart_item.total
    




class CartItemDeleteApiView(generics.DestroyAPIView):
    serializer_class = CartSerializer
    lookup_field = 'cart_id'
    
    def get_object(self):
        cart_id = self.kwargs['cart_id'] 
        item_id = self.kwargs['item_id']    
        user_id = self.kwargs.get('user_id')
        
        if user_id:       
            user = User.objects.get(id=user_id)
            return Cart.objects.get(id=item_id, cart_id=cart_id, user=user)
        else:
            return Cart.objects.get(cart_id=cart_id, id=item_id)
        


class CreateOrderView(generics.CreateAPIView):
    serializer_class = CartOrderSerializer
    queryset = CartOrder.objects.all()
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        payload = request.data

        full_name = payload['full_name']
        email = payload['email']
        mobile = payload['mobile']
        address = payload['address']
        city = payload['city']
        state = payload['state']
        country = payload['country']
        cart_id = payload['cart_id']
        user_id = payload['user_id']

        print("user_id ===============", user_id)

        if user_id != 0:
            user = User.objects.filter(id=user_id).first()
        else:
            user = None

        cart_items = Cart.objects.filter(cart_id=cart_id)

        total_shipping = Decimal(0.0)
        total_tax = Decimal(0.0)
        total_service_fee = Decimal(0.0)
        total_sub_total = Decimal(0.0)
        total_initial_total = Decimal(0.0)
        total_total = Decimal(0.0)

        # with transaction.atomic():

        order = CartOrder.objects.create(
            # sub_total=total_sub_total,
            # shipping_amount=total_shipping,
            # tax_fee=total_tax,
            # service_fee=total_service_fee,
            buyer=user,
            # payment_status="processing",
            full_name=full_name,
            email=email,
            mobile=mobile,
            address=address,
            city=city,
            state=state,
            country=country
        )

        for c in cart_items:
            CartOrderItem.objects.create(
                order=order,
                product=c.product,
                qty=c.qty,
                color=c.color,
                size=c.size,
                price=c.price,
                sub_total=c.sub_total,
                shipping_amount=c.shipping_amount,
                tax_fee=c.tax_fee,
                service_fee=c.service_fee,
                total=c.total,
                initial_total=c.total,
                vendor=c.product.vendor
            )

            total_shipping += Decimal(c.shipping_amount)
            total_tax += Decimal(c.tax_fee)
            total_service_fee += Decimal(c.service_fee)
            total_sub_total += Decimal(c.sub_total)
            total_initial_total += Decimal(c.total)
            total_total += Decimal(c.total)

            order.vendor.add(c.product.vendor)

            

        order.sub_total=total_sub_total
        order.shipping_amount=total_shipping
        order.tax_fee=total_tax
        order.service_fee=total_service_fee
        order.initial_total=total_initial_total
        order.total=total_total

        
        order.save()

        return Response( {"message": "Order Created Successfully", 'order_oid':order.oid}, status=status.HTTP_201_CREATED)

        



class CheckoutView(generics.RetrieveAPIView):
    serializer_class = CartOrderSerializer
    lookup_field = 'order_oid'  

    def get_object(self):
        order_oid = self.kwargs['order_oid']
        order = get_object_or_404(CartOrder, oid=order_oid)
        return order
            


class CouponApiView(generics.CreateAPIView):
    serializer_class = CartOrderSerializer

    def create(self, request, *args, **kwargs):
        payload = request.data

        order_oid = payload['order_oid']
        coupon_code = payload['coupon_code']
        print("order_oid =======", order_oid)
        print("coupon_code =======", coupon_code)

        order = CartOrder.objects.get(oid=order_oid)
        coupon = Coupon.objects.filter(code__iexact=coupon_code, active=True).first()
        
        if coupon:
            order_items = CartOrderItem.objects.filter(order=order, vendor=coupon.vendor)
            if order_items:
                for i in order_items:
                    print("order_items =====", i.product.title)
                    if not coupon in i.coupon.all():
                        discount = i.total * coupon.discount / 100
                        
                        i.total -= discount
                        i.sub_total -= discount
                        i.coupon.add(coupon)
                        i.saved += discount
                        i.applied_coupon = True

                        order.total -= discount
                        order.sub_total -= discount
                        order.saved += discount

                        i.save()
                        order.save()
                        return Response( {"message": "Coupon Activated"}, status=status.HTTP_200_OK)
                    else:
                        return Response( {"message": "Coupon Already Activated"}, status=status.HTTP_200_OK)
            return Response( {"message": "Order Item Does Not Exists"}, status=status.HTTP_200_OK)
        else:
            return Response( {"message": "Coupon Does Not Exists"}, status=status.HTTP_404_NOT_FOUND)

