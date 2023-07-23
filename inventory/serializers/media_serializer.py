from rest_framework.serializers import ModelSerializer
from inventory import models


class MediaSerializer(ModelSerializer):
    class Meta:
        model = models.Media
        exclude = ['created_at', 'updated_at']
