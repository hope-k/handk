from dj_rest_auth.registration.views import RegisterView, LoginView
from custom_user.serializers import CustomRegisterSerializer, CustomLoginSerializer
from django.contrib.auth.backends import BaseBackend


class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer


class CustomLoginView(LoginView):
    serializer_class = CustomLoginSerializer
