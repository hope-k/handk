from rest_framework import serializers
from inventory import models
from inventory.serializers.media_serializer import MediaSerializer
from .product_attribute_values_serializer import ProductAttributeValuesSerializer


class ProductInventorySerializer(serializers.ModelSerializer):
    specification = ProductAttributeValuesSerializer(
        many=True, read_only=True, source='attribute_values')
    images = MediaSerializer(many=True)
    discount_percentage = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.ProductInventory
        # add all fields and product relationship
        fields = [
            'id',
            'sku',
            'upc',
            'specification',
            'retail_price',
            'sale_price',
            'is_active',
            'is_default',
            'images',
            'discount_percentage'
        ]
        depth = 2

    def get_discount_percentage(self, inventory):
        retail_price = inventory.retail_price
        sale_price = inventory.sale_price

        if retail_price and sale_price:
            discount_percent = (1 - sale_price / retail_price) * 100
            return round(discount_percent)
        else:
            return 0
