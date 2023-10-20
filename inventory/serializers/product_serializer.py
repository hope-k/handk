from rest_framework import serializers
from inventory import models
from .product_inventory_serializer import ProductInventorySerializer
from .brand_serializer import BrandSerializer
from django.db.models.aggregates import Avg
from .category_serializer import CategorySerializer


class ProductSerializer(serializers.ModelSerializer):
    inventory = ProductInventorySerializer(many=True, source='inventories')
    brand = BrandSerializer()
    # todo: num_of_ratings
    # todo: avg_rating
    # num_of_rating = serializers.SerializerMethodField()
    avg_rating = serializers.SerializerMethodField()
    total_rating = serializers.SerializerMethodField()
    min_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True)
    category = CategorySerializer(many=True)
    is_in_wishlist = serializers.BooleanField(read_only=True)

    class Meta:
        model = models.Product
        fields = [
            'id',
            'name',
            'is_in_wishlist',
            'min_price',
            'features',
            'uuid',
            'brand',
            'slug',
            'avg_rating',
            'total_rating',
            'description',
            'category',
            'inventory',
        ]
        depth = 1

    def get_avg_rating(self, product: models.Product):
        avg_rating = product.reviews.aggregate(rating=Avg('rating'))['rating']
        return int(avg_rating) if avg_rating else 0

    def get_total_rating(self, product: models.Product):
        return product.reviews.count()
