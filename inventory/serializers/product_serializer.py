from rest_framework.serializers import ModelSerializer
from inventory import models
from .product_inventory_serializer import ProductInventorySerializer
from .brand_serializer import BrandSerializer


class ProductSerializer(ModelSerializer):
    inventory = ProductInventorySerializer(many=True, source='inventories')
    brand = BrandSerializer()

    class Meta:
        model = models.Product
        fields = [
            'id',
            'name',
            'uuid',
            'brand',
            'slug',
            'description',
            'category',
            'inventory',
        ]
        depth = 1
