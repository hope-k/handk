from rest_framework.viewsets import ModelViewSet, GenericViewSet
from inventory.serializers.wishlist_serializer import WishlistSerializer
from custom_user.serializers import UserSerializer
from custom_user.models import CustomUser
from inventory.serializers.order_serializer import OrderSerializer, OrderItemSerializer, CreateOrderSerializer, UpdateOrderSerializer
from inventory.models import CartItem
from inventory.serializers.cart_serializers import CartSerializer, CartItemSerializer, AddCartItemSerializer, UpdateCartItemSerializer
from inventory.serializers.review_serializer import ReviewSerializer
from inventory import models
from inventory.filters import ProductFilter
from inventory.permission import AdminPermission
from inventory.serializers.brand_serializer import BrandSerializer
from inventory.serializers.category_serializer import CategorySerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import mixins
# ! SERIALIZERS
from inventory.serializers.product_serializer import ProductSerializer
from inventory.serializers.product_inventory_serializer import (
    ProductInventorySerializer
)
from custom_user.models import ShippingAddress
from inventory.serializers.shipping_address_serializer import ShippingAddressSerializer
from permissions import custom_permissions
from permissions.assign_permissions import assign_permissions
from rest_framework import permissions


class Products(ModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    permission_classes = [AdminPermission]
    filterset_class = ProductFilter
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter
    ]
    search_fields = [
        '$name',
        '^brand__name',
        '^product_type__name',
    ]


class ProductInventory(ModelViewSet):
    queryset = models.ProductInventory.objects.all()
    serializer_class = ProductInventorySerializer
    permission_classes = [AdminPermission]
    lookup_field = 'sku'
    # filterset_class = ProductInventoryFilter
    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter,
    ]
    ordering_fields = ['store_price']
    ordering = ['store_price']


class Category(ModelViewSet):
    queryset = models.Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    pagination_class = None

    # ! this is the only way to get the root categories
    # ! detail is false because we are not getting a single category
    # ! if detail is true, we will get a single category hence access to the
    # ! slug param
    @action(detail=False, methods=['get'])
    def root(self, request):
        queryset = self.get_queryset().filter(parent=None)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class Brand(ModelViewSet):
    queryset = models.Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [AdminPermission]
    pagination_class = None


class ReviewView(ModelViewSet):
    queryset = models.Review.objects.all()
    serializer_class = ReviewSerializer


class CartView(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    # ! prefect product here to prevent multiple queries when serializer is
    # ! summing up the total price in cart
    queryset = models.Cart.objects.prefetch_related(
        'cart_items__product').all()
    serializer_class = CartSerializer
    permission_classes = [custom_permissions.CreateForMyAccount]

    def get_queryset(self):
        return models.Cart.objects.filter(user=self.request.user)


class CartItemView(ModelViewSet):
    permission_classes = [custom_permissions.IsAuthenticatedAndIsObjectOwner]
    http_method_names = ['get', 'patch', 'delete', 'post', 'options', 'head']
    assign_perms = [
        'inventory.delete_cartitem',
        'inventory.view_cartitem',
        'inventory.change_cartitem'
    ]

    # ! custom queryset to get the cart_pk from the nested route url

    def get_queryset(self):
        # ! getting only items of a particular cart.
        # ? checkout to django extension implementation as well
        return CartItem.objects.filter(cart=self.kwargs['cart_pk'], cart__user=self.request.user)

    def get_serializer_class(self):
        if (self.request.method == 'POST'):
            return AddCartItemSerializer
        elif (self.request.method == 'PATCH'):
            return UpdateCartItemSerializer
        else:
            return CartItemSerializer

    def get_serializer_context(self):
        return {
            'cart_id': self.kwargs['cart_pk']
        }

    def get_permission_type(self):
        request = self.request
        if request.method == 'PATCH':
            return 'inventory.change_cartitem'
        elif request.method == 'DELETE':
            return 'inventory.delete_cartitem'
        return 'inventory.view_cartitem'

    # ? Best place to do something
    # ? before caaling save on serializer after the whole creation process
    def perform_create(self, serializer):
        cart_item = serializer.save()
        assign_permissions(self.request.user, cart_item, self.assign_perms)


class ShippingAddressView(ModelViewSet):
    queryset = ShippingAddress.objects.all()
    serializer_class = ShippingAddressSerializer
    permission_classes = [
        custom_permissions.IsAuthenticatedAndIsObjectOwner,
        custom_permissions.CreateForMyAccount
    ]
    # ? permissions to assign when creating the object
    assign_perms = [
        'custom_user.delete_shippingaddress',
        'custom_user.view_shippingaddress',
        'custom_user.change_shippingaddress'
    ]

    # ? permission to check for based on the request method.
    # ? this is to make the permission(IsAuthenticatedAndIsOwner)
    # ? dynamic so i can use it for different viewset
    def get_permission_type(self):
        request = self.request
        if request.method in ['PUT', 'PATCH']:
            return 'custom_user.change_shippingaddress'
        elif request.method == 'DELETE':
            return 'custom_user.delete_shippingaddress'
        return 'custom_user.view_shippingaddress'

    def get_queryset(self):
        # ! filtering based on current user and not user_pk in param because user id is not
        # ! uuidv4 and any id passed in the url param will be returned
        return ShippingAddress.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        shipping_address = serializer.save()
        assign_permissions(self.request.user, shipping_address, self.assign_perms)


class OrderView(ModelViewSet):
    queryset = models.Order.objects.all()
    permission_classes = [custom_permissions.CreateForMyAccount]
    http_method_names = ['post', 'patch', 'get', 'delete']
    assign_perms = [
        'inventory.delete_orderitem',
        'inventory.view_orderitem',
        'inventory.change_orderitem'
    ]
    # ? THE CREATE METHOD EXECUTES THE SAVE METHOD OF THE SERIALIZER
    # ? WHICH IS RESPONSIBLE FOR CREATING THE ORDER AND ORDER ITEMS ATOMICALLY(Transaction)

    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(
            data=request.data,
            context={
                'user_pk': self.request.user,
                'assign_perms': self.assign_perms
            }
        )
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def get_queryset(self):
        return models.Order.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if (self.request.method == 'POST'):
            return CreateOrderSerializer
        elif (self.request.method == 'PATCH'):
            return UpdateOrderSerializer
        else:
            return OrderSerializer


class OrderItemView(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet
):
    serializer_class = OrderItemSerializer
    permission_classes = [custom_permissions.IsAuthenticatedAndIsObjectOwner]

    # ! custom queryset to get the cart_pk from the nested route url

    def get_queryset(self):
        # ! using order_pk to filter cause it is uuidv4 and not easy to guess
        # ! since to order_pk in the url is the current user order
        return models.OrderItem.objects.filter(order=self.kwargs['order_pk'])

    def get_permission_type(self):
        request = self.request
        if request.method in ['PUT', 'PATCH']:
            return 'inventory.change_orderitem'
        elif request.method == 'DELETE':
            return 'inventory.delete_orderitem'
        return 'inventory.view_orderitem'


class WishlistView(ModelViewSet):
    queryset = models.Wishlist.objects.all()
    serializer_class = WishlistSerializer
    permission_classes = [custom_permissions.IsAuthenticatedAndIsObjectOwner]
    assign_perms = [
        'inventory.delete_orderitem',
        'inventory.view_orderitem',
        'inventory.change_orderitem'
    ]

    def get_queryset(self):
        return models.Wishlist.objects.filter(user=self.request.user)

    def get_permission_type(self):
        request = self.request
        if request.method in ['PUT', 'PATCH']:
            return 'inventory.change_wishlist'
        elif request.method == 'DELETE':
            return 'inventory.delete_wishlist'
        return 'inventory.view_wishlist'

    def perform_create(self, serializer):
        wishlist = serializer.save()
        assign_permissions(self.request.user, wishlist, self.assign_perms)


class UserView(mixins.ListModelMixin, GenericViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return CustomUser.objects.filter(pk=user.pk)
