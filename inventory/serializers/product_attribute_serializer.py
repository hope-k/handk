from rest_framework.serializers import ModelSerializer
from inventory import models


class ProductAttributeSerializer(ModelSerializer):
    class Meta:
        model = models.ProductAttribute
        exclude = ['id']
