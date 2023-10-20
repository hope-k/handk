from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, AbstractBaseUser, PermissionsMixin
from storage.custom_cloudinary_storage import CustomStorage
from cloudinary.models import CloudinaryField
from rest_framework_simplejwt.tokens import RefreshToken

# ? using base user manager because it uses email not username


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email is required')

        if not password:
            raise ValueError('Password is required')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    AUTH_PROVIDERS = (
        ('facebook', 'facebook'),
        ('google', 'google'),
        ('email', 'email')
    )
    username = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    first_name = models.CharField(max_length=256, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    avatar = models.ImageField(
        upload_to='hnk/users/avatars/',
        verbose_name='User Image',
        storage=CustomStorage(),
        null=True,
        blank=True
    )
    provider = models.CharField(
        choices=AUTH_PROVIDERS,
        max_length=25,
        null=True,
        default='email'
    )
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'auth_user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def delete(self, *args, **kwargs):
        self.avatar.storage.delete()
        super().delete(*args, **kwargs)

    def generate_tokens(user):
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        return {
            'refresh': str(refresh),
            'access': str(access),
        }


class ShippingAddress(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='shipping_addresses')
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    is_default = models.BooleanField(default=False)
