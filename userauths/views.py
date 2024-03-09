import random
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User, Profile
from rest_framework.permissions import AllowAny
from rest_framework import generics
from .serializers import  MyTokenObtainPairSerializer, RegisterSerializer, UserSerializer
# Create your views here.


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class =MyTokenObtainPairSerializer
    


class RegisterView(generics.CreateAPIView):
    permission_classes = (AllowAny, )    
    serializer_class = RegisterSerializer
    

def generate_otp():
        otp =random.randint(100000, 999999)
        return otp
class PasswordResetEmailVerify(generics.RetrieveAPIView):  
    permission_classes = (AllowAny, )
    serializer_class =  UserSerializer
    
    def get_object(self):
        email = self.kwargs['email']
        user = User.objects.get(email=email)
        if user:
            otp = generate_otp()

            user.otp = otp
            # link for frontend
            link = f'http://localhost:5143/create-new-password?otp={otp}&uidb64={user.id}'
            user.save()
            # send email
            

class PasswordChangeView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
    
    def create(self, request, *args, **kwargs):
        payload = request.data
        
        otp = payload['otp']
        uidb64 = payload['uidb64']
        reset_token = payload['reset_token']
        password = payload['password']

        print("otp ======", otp)
        print("uidb64 ======", uidb64)
        print("reset_token ======", reset_token)
        print("password ======", password)

        user = User.objects.get(id=uidb64, otp=otp)
        if user:
            user.set_password(password)
            user.otp = ""
            user.reset_token = ""
            user.save()

            
            return Response( {"message": "Password Changed Successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response( {"message": "An Error Occured"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
