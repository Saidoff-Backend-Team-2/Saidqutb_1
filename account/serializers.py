from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from django.utils.translation import gettext_lazy as _


class UserRegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['user_type', 'full_name', 'username', 'email', 'password', 'phone_number', 'company_name', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': False},
            'company_name': {'required': False},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError(
                _('Passwords do not match')
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginRequestSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        try:
            user = User.objects.get(username=attrs['username'])
            if not user.check_password(attrs['password']):
                raise serializers.ValidationError(_('User password is incorrect'))
            return attrs
        except User.DoesNotExist:
            raise serializers.ValidationError(_('User does not exist'))


class UserLoginResponseSerializer(serializers.Serializer):
    access = serializers.CharField(required=True)
    refresh = serializers.CharField(required=True)


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['full_name', 'email', 'username', 'phone_number','company_name']
        extra_kwargs = {
            'email': {'required': False},
            'username': {'required': False},
            'full_name': {'required': False},
        }

    def validate_email(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError('Email is already in use.')
        return value

    def validate_username(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError('Username is already in use.')
        return value

