from rest_framework import serializers
from inventory.models import Order, OrderItem, CartItem, Cart
from permissions.assign_permissions import assign_permissions
from django.db import transaction
from rest_framework.validators import ValidationError
from django.db.models import Sum, F


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'id',
            'total_order',
            'order_items',
            'created_at',
            'updated_at'
        ]
    total_order = serializers.SerializerMethodField()

    def get_total_order(self, order):
        total_order = order.order_items.aggregate(
            total=Sum(F('quantity') * F('product__sale_price')))['total']
        #  sum([item.quantity * item.product.sale_price for item in order.order_items.all()])
        return total_order if total_order is not None else 0

    # def get_total_order(self, order):
    #     # Calculate the total order for each Order instance using annotate
    #     total_order = order.order_items.annotate(
    #         item_total=F('quantity') * F('product__sale_price')
    #     ).aggregate(total=Sum('item_total'))['total']
    #     return total_order if total_order is not None else 0


class CreateOrderSerializer(serializers.ModelSerializer):
    cart = serializers.UUIDField()

    class Meta:
        model = Order
        fields = ['cart', 'user']

    def validate_cart(self, cart: serializers.UUIDField):
        if CartItem.objects.filter(cart=cart).count() == 0:
            raise ValidationError('Cart is empty', 403)
        return cart

    def save(self, **kwargs):
        with transaction.atomic():
            user = self.context['user_pk']
            cart_id = self.validated_data['cart']
            assign_perms = self.context['assign_perms']
            order = Order.objects.create(user=user)

            print('HERE-->>', order)
            cart_items = CartItem.objects.select_related(
                'product_inventory').filter(cart=cart_id)
            order_items = [
                OrderItem(
                    order=order,
                    product=item.product_inventory,
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                    status='pending'
                ) for item in cart_items
            ]
            OrderItem.objects.bulk_create(order_items)

            for item in order_items:
                assign_permissions(user, item, assign_perms)

            Cart.objects.filter(pk=cart_id).delete()
            return order
