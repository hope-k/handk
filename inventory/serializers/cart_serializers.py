from rest_framework import serializers
from inventory import models
from .product_inventory_serializer import ProductInventorySerializer


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductInventorySerializer()
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart_item: models.CartItem):
        return cart_item.quantity * cart_item.product.store_price

    class Meta:
        model = models.CartItem
        fields = [
            'id',
            'quantity',
            'total_price',
            'product'
        ]

class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    cart_total_price = serializers.SerializerMethodField()

    def get_cart_total_price(self, cart: models.Cart):
        # ! the list comprehension return a list of total prices
        # ! for each item in the cart
        return sum([item.quantity * item.product.store_price for item in cart.cart_items.all()])

    class Meta:
        model = models.Cart
        fields = [
            'id',
            'user',
            'cart_total_price',
            'created_at',
            'items',
        ]


class AddCartItemSerializer(serializers.ModelSerializer):
    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product = self.validated_data['product']
        quantity = self.validated_data['quantity']
        try:
            # increase item in cart quantity
            cart_item = models.CartItem.objects.get(
                cart=cart_id, product=product)
            cart_item.quantity += quantity
            self.instance = cart_item.save()
        except models.CartItem.DoesNotExist:
            # create new item
            # ? object created has to stored in self.instance
            self.instance = models.CartItem.objects.create(
                cart_id=cart_id,
                **self.validated_data
            )
        return self.instance

    class Meta:
        model = models.CartItem
        fields = [
            'id',
            'quantity',
            'product'
        ]


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CartItem
        fields = [
            'quantity'
        ]
