from enum import unique
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import  ValidationError
from rest_framework_simplejwt.tokens import RefreshToken


class User(AbstractUser):
    class UserType(models.TextChoices):
        LEGAL = 'legal', _('LEGAL')
        INDIVIDUAL = 'individual', _('INDIVIDUAL')

    full_name = models.CharField(_('full name'), max_length=255)
    email = models.EmailField(_('email'), unique=True)
    username = models.CharField(_('username'), max_length=255, unique=True)
    phone_number = PhoneNumberField(_('phone_number'), unique=True)
    password = models.CharField(_('password'), max_length=255)
    user_type = models.CharField(
        _('user type'),
        max_length=10,
        choices=UserType.choices,
        default=UserType.INDIVIDUAL
    )
    company_name = models.CharField(_('company name'), max_length=255, null=True, blank=True)

    def clean(self):
        super().clean()
        if self.user_type == self.UserType.LEGAL and not self.company_name:
            raise ValidationError({'company_name': _('Company name is required for legal entities')})

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def get_token(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


class TelegramUser(models.Model):
    user = models.OneToOneField(User,null=True, blank=True, on_delete=models.CASCADE, related_name='telegram_user')
    telegram_id = models.CharField(_('telegram_id'), max_length=255, unique=True)
    telegram_user = models.CharField(_('telegram username'), max_length=255, blank=True, null=True)

