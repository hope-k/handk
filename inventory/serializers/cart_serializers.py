from rest_framework import serializers
from inventory import models
from django.db.models import Sum, F
from utils.validate_attribute_values import validate_attribute_values
from .product_attribute_values_serializer import ProductAttributeValuesSerializer


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CartItem
        fields = '__all__'

    total_price = serializers.SerializerMethodField()
    specification = ProductAttributeValuesSerializer(
        many=True, read_only=True, source='attribute_values')
    discount_percentage = serializers.SerializerMethodField(read_only=True)
    product_name = serializers.CharField(
        source='product_inventory.product.name', read_only=True)
    product_slug = serializers.CharField(
        source='product_inventory.product.slug', read_only=True)
    sale_price = serializers.CharField(
        source='product_inventory.sale_price', read_only=True)

    def get_total_price(self, cart_item: models.CartItem):
        return cart_item.quantity * cart_item.unit_price

    def get_discount_percentage(self, cart_item):
        retail_price = cart_item.product_inventory.retail_price
        sale_price = cart_item.product_inventory.sale_price

        if retail_price and sale_price:
            discount_percent = (1 - sale_price / retail_price) * 100
            return round(discount_percent)
        else:
            return 0


# todo do a get or create for cart
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cart
        fields = [
            'id',
            'user',
            'cart_total_price',
            'created_at',
            'items_count'
        ]
    id = serializers.UUIDField(read_only=True)
    cart_total_price = serializers.SerializerMethodField()
    items_count = serializers.SerializerMethodField()

    def get_cart_total_price(self, cart):
        total_price = cart.cart_items.aggregate(
            total=Sum(F('quantity') * F('unit_price'))
        )['total']
        return total_price if total_price is not None else 0

    def get_items_count(self, cart):
        count = cart.user.cart.cart_items.count()
        return count if count is not None else 0


class AddCartItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CartItem
        fields = '__all__'

    def validate(self, data):

        chosen_attributes = data['attribute_values']
        product_inv = data['product_inventory']

        try:
            product_inventory = models.ProductInventory.objects.get(
                pk=product_inv.id)
            for chosen_attribute in chosen_attributes:
                is_valid_attribute = validate_attribute_values(
                    chosen_attribute, product_inventory)
                if not is_valid_attribute:
                    raise serializers.ValidationError(
                        f"Selected product does not have the chosen {chosen_attribute.product_attribute.name}: {chosen_attribute.description} - {chosen_attribute.attribute_value} "
                    )
        except models.ProductInventory.DoesNotExist:
            raise serializers.ValidationError("Product inventory not found.")
        return data

    def save(self, **kwargs):
        cart_id = self.context['cart_pk']
        product_inventory = self.validated_data['product_inventory']
        quantity = self.validated_data['quantity']
        chosen_attributes = self.validated_data['attribute_values']
        unit_price = self.validated_data['unit_price']
        try:
            # increase item in cart quantity
            # todo check if the attribute given if the same if so increase the quantity else add the same product with the differnt attributes
            # todo, first approach(simple one) - in the cart item query , try to get/filter out the chosen attrubutes as well
            cart_item = models.CartItem.objects.get(
                cart=cart_id,
                product_inventory=product_inventory,
                attribute_values__in=chosen_attributes,
                unit_price=unit_price
            )
            cart_item.quantity += quantity
            self.instance = cart_item.save()
        except models.CartItem.DoesNotExist:
            # create new item
            # ? object created has to stored in self.instance so that instance can be returned from the try except block regardless of the outcome in the try except block
            created_item = models.CartItem.objects.create(
                cart_id=cart_id,
                product_inventory=product_inventory,
                quantity=quantity,
                unit_price=unit_price
            )
            created_item.attribute_values.set(chosen_attributes)
            self.instance = created_item
        return self.instance


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CartItem
        fields = [
            'quantity'
        ]
