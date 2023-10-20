from rest_framework import generics
from rest_framework import status
from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework.validators import ValidationError
from django.contrib.auth.hashers import make_password
from .GoogleAuthSerializer import GoogleAuthSerializer
from rest_framework.response import Response
from allauth.account.models import EmailAddress
from users.serializers import UserSerializer


class GoogleLoginView(generics.CreateAPIView):
    serializer_class = GoogleAuthSerializer
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        user_model = get_user_model()
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        provider = serializer.validated_data['provider']
        aud = serializer.validated_data['aud']

        user = user_model.objects.filter(
            email=serializer.validated_data['email'])

        if user.exists():

            if aud == settings.GOOGLE_CLIENT_ID:  # ? check if audience is google client id i set in settings
                if provider == user[0].provider:
                    authenticated_user = authenticate(
                        email=serializer.validated_data['email'],
                        password=settings.SOCIAL_AUTH_SECRET_KEY
                    )
                    if authenticated_user:
                        serialized_authenticated_user = UserSerializer(
                            authenticated_user).data
                        res_data = {
                            'access_token': user_model.generate_tokens(authenticated_user)['access'],
                            'refresh_token': user_model.generate_tokens(authenticated_user)['refresh'],
                            **serialized_authenticated_user
                        }
                        return Response(res_data, status=status.HTTP_200_OK)
                    else:
                        raise ValidationError('Invalid credentials', 401)
                else:
                    raise ValidationError(
                        f"Please login with {user[0].provider} account")
            else:
                raise ValidationError('Invalid credentials', 401)
        else:
            if aud == settings.GOOGLE_CLIENT_ID:
                user = user_model.objects.create(
                    email=serializer.validated_data['email'],
                    provider=serializer.validated_data.get(
                        'provider', 'google'),
                    first_name=serializer.validated_data['first_name'],
                    last_name=serializer.validated_data['last_name'],
                    # ? This is optional get return None if not found
                    username=serializer.validated_data.get('username'),
                    password=make_password(settings.SOCIAL_AUTH_SECRET_KEY),
                    avatar=serializer.validated_data['avatar'],
                )
                email_verified = serializer.validated_data.get(
                    'email_verified', False)
                if email_verified:
                    EmailAddress.objects.create(
                        user=user,
                        email=user.email,
                        verified=True,
                        primary=True
                    )

                user.save()
                authenticated_user = authenticate(
                    email=serializer.validated_data['email'],
                    password=settings.SOCIAL_AUTH_SECRET_KEY
                )

                deserialized_authenticated_user = UserSerializer(
                    authenticated_user).data
                res_data = {
                    'access': user_model.generate_tokens(authenticated_user)['access'],
                    'refresh': user_model.generate_tokens(authenticated_user)['refresh'],
                    'user': deserialized_authenticated_user
                }

                return Response(res_data, status=status.HTTP_200_OK)
            else:
                raise ValidationError('Invalid credentials', 401)
