from rest_framework import serializers


class GoogleAuthSerializer(serializers.Serializer):
    provider = serializers.CharField(max_length=255, required=True)
    email_verified = serializers.BooleanField(required=True)
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(max_length=255, required=True)
    last_name = serializers.CharField(max_length=255, required=True)
    username = serializers.CharField(max_length=255, required=False)
    aud = serializers.CharField(max_length=255, required=True)
    avatar = serializers.URLField(required=True)