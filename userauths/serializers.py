from django.contrib.auth.password_validation import validate_password
from .models import User, Profile
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['full_name'] = user.full_name
        token['username'] = user.username
        token['email'] = user.email
        try:
            token['vendor_id'] = user.vendor.id
        except:
            token['vendor_id'] = 0
        return token
    

class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True
                                      )

    class Meta:
        model = User
        fields = ('username', 'email', 'full_name', 'phone' 'password1', 'password2')
        
        
    def validate(self, attrs):
        if attrs.get('password1') != attrs.get('password2'):
            raise serializers.ValidationError({'password': 'passwords must be the same'})
        return attrs
    
    
    def create(self, validated_data):
        user = User.objects.create(username= validated_data['username'], email= validated_data['email'], full_name= validated_data['full_name'], phone= validated_data['phone'])
    
        email_user, mobile =  user.email.split('@')
        user.set_password(validate_password['password'])
        user.save()
        return user   

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'        
        
    def to_representation(self, instance):
        return super(ProfileSerializer, self).to_representation(instance)    
        representation['user'] = instance.user.full_name
        return representation