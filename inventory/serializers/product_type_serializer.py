from rest_framework.serializers import ModelSerializer
from inventory import models


class ProductTypeSerializer(ModelSerializer):
    class Meta:
        model = models.ProductType
        fields = [
            'name'
        ]
