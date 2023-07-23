from rest_framework.serializers import ModelSerializer
from inventory import models


class BrandSerializer(ModelSerializer):
    class Meta:
        model = models.Brand
        fields = [
            'id',
            'name'
        ]
