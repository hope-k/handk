from rest_framework import serializers
from .models import User, ShippingAddress
from allauth.account import app_settings as allauth_account_settings
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer, TokenSerializer, JWTSerializer
from django.core.exceptions import ValidationError as DjangoValidationError
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email


class CustomJWTSerializer(JWTSerializer):
    pass


class CustomTokenSerializer(TokenSerializer):
    pass


class CustomLoginSerializer(LoginSerializer):
    username = None
    email = serializers.EmailField(
        required=allauth_account_settings.EMAIL_REQUIRED)
    password = serializers.CharField(write_only=True)

    def validate_email(self, email):
        provider = 'email'
        user = User.objects.filter(email=email).first()
        if user:
            if not user.is_active:
                raise serializers.ValidationError(
                    'User account is disabled.')
            if provider != user.provider:
                raise serializers.ValidationError(
                    'Please continue your login using ' + user.provider + ' account')

        return email


class CustomRegisterSerializer(RegisterSerializer):
    username = None
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(
        required=allauth_account_settings.EMAIL_REQUIRED)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate_email(self, email):
        provider = 'email'
        user = User.objects.filter(email=email).first()
        if user:
            if provider != str(user.provider):
                raise serializers.ValidationError(
                    'Please continue your login using ' + user.provider + ' account')

        return super().validate_email(email)

    def get_cleaned_data(self):
        return {
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user = adapter.save_user(request, user, self, commit=False)
        if "password1" in self.cleaned_data:
            try:
                adapter.clean_password(
                    self.cleaned_data['password1'], user=user)
            except DjangoValidationError as exc:
                raise serializers.ValidationError(
                    detail=serializers.as_serializer_error(exc)
                )
        user.save()
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user


class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    email_verified = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = '__all__'

    def get_email_verified(self, user):
        return user.emailaddress_set.filter(verified=True).exists()
