from rest_framework import serializers
from inventory import models


class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Wishlist
        fields = '__all__'


class WishlistItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.WishlistItem
        fields = '__all__'


class CreateWishlistItemSerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=models.Product.objects.all())
    wishlist = serializers.PrimaryKeyRelatedField(
        queryset=models.Wishlist.objects.all())

    def create(self, validated_data):
        try:
            wishlist = models.WishlistItem.objects.get(
                wishlist=validated_data['wishlist'],
                product=validated_data['product']
            )
            wishlist.delete()

            self.instance = models.WishlistItem()
        except models.WishlistItem.DoesNotExist:
            wishlist = models.WishlistItem.objects.create(
                wishlist=validated_data['wishlist'],
                product=validated_data['product']
            )
            self.instance = wishlist
        return self.instance
