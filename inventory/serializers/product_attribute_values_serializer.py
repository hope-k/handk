from rest_framework.serializers import ModelSerializer
from inventory import models
from .product_attribute_serializer import ProductAttributeSerializer


class ProductAttributeValuesSerializer(ModelSerializer):
    product_attribute = ProductAttributeSerializer()

    class Meta:
        model = models.ProductAttributeValue
        exclude = [
            'id',
        ]
