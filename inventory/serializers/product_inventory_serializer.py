from rest_framework.serializers import ModelSerializer
from inventory import models
from inventory.serializers.media_serializer import MediaSerializer
from .product_type_serializer import ProductTypeSerializer
from .product_attribute_values_serializer import ProductAttributeValuesSerializer
from .brand_serializer import BrandSerializer


class ProductInventorySerializer(ModelSerializer):
    attribute_values = ProductAttributeValuesSerializer(many=True)
    inventory_images = MediaSerializer(many=True, source='images')

    class Meta:
        model = models.ProductInventory
        # add all fields and product relationship
        fields = [
            'id',
            'sku',
            'upc',
            'retail_price',
            'sale_price',
            'store_price',
            'is_active',
            'is_default',
            'attribute_values',
            'inventory_images',
        ]
        depth = 2
