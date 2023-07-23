from rest_framework import serializers
from inventory.models import Order, OrderItem, CartItem, Cart
from permissions.assign_permissions import assign_permissions
from django.db import transaction
from rest_framework.validators import ValidationError
from action_serializer import ModelActionSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        exclude = ['order']


class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'status'
        ]

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)
    total_order = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'id',
            'status',
            'total_order',
            'order_items',
            'created_at',
            'updated_at'
        ]


    def get_total_order(self, order):
        return sum([item.quantity * item.product.sale_price for item in order.order_items.all()])


class CreateOrderSerializer(serializers.Serializer):
    cart = serializers.UUIDField()

    class Meta:
        model = Order
        fields = ['cart']

    def validate_cart(self, cart: serializers.UUIDField):
        if CartItem.objects.filter(cart=cart).count() == 0:
            raise ValidationError('Cart is empty', 403)
        return cart

    def save(self, **kwargs):
        with transaction.atomic():
            user = self.context['user_pk']
            cart_id = self.validated_data['cart']
            assign_perms = self.context['assign_perms']

            order = Order.objects.create(
                user=user
            )
            cart_items = CartItem.objects.select_related('product').filter(cart=cart_id)
            order_items = [
                OrderItem(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    unit_price=item.product.sale_price
                ) for item in cart_items
            ]

            OrderItem.objects.bulk_create(order_items)

            for item in order_items:
                assign_permissions(user, item, assign_perms)

            Cart.objects.filter(pk=cart_id).delete()
            return order
