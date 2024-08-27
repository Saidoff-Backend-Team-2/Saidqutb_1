from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from django.utils.translation import gettext_lazy as _


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_type', 'full_name', 'username', 'email', 'password', 'phone_number']
        extra_kwargs = {
            'email': {'required': False, 'allow_blank': True},
            'password': {'write_only': True}
        }

    def validate(self, data):
        if User.objects.filter(email=data.get('email')).exists():
            raise serializers.ValidationError({'email': _('This email is already registered.')})
        if data['user_type'] == User.UserType.LEGAL and not data.get('company_name'):
            raise serializers.ValidationError({
                'company_name': _('Company name is required for legal entities.')
            })
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            user_type=validated_data['user_type'],
            full_name=validated_data['full_name'],
            username=validated_data['username'],
            email=validated_data.get('email'),
            phone_number=validated_data['phone_number'],
            password=validated_data['password'],
            company_name=validated_data.get('company_name')
        )
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    pass


class EmailLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate(self, data):
        email = data.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({'email': _('User with this email was not found.')})

        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }