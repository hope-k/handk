from dj_rest_auth.registration.views import RegisterView, LoginView
from users.serializers import CustomRegisterSerializer, CustomLoginSerializer


class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer


class CustomLoginView(LoginView):
    serializer_class = CustomLoginSerializer
