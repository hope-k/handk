from rest_framework.viewsets import ModelViewSet, GenericViewSet, mixins
from inventory.serializers.wishlist_serializer import WishlistSerializer, WishlistItemSerializer, CreateWishlistItemSerializer
from users.models import User
from users.serializers import UserSerializer
from inventory.serializers.order_serializer import OrderSerializer, OrderItemSerializer, CreateOrderSerializer
from inventory.models import CartItem
from inventory.serializers.cart_serializers import CartSerializer, CartItemSerializer, AddCartItemSerializer, UpdateCartItemSerializer
from inventory.serializers.review_serializer import ReviewSerializer
from inventory import models
from inventory.filters import ProductFilter
from inventory.serializers.brand_serializer import BrandSerializer
from inventory.serializers.category_serializer import CategorySerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from rest_framework.response import Response
# ! SERIALIZERS
from inventory.serializers.product_serializer import ProductSerializer
from inventory.serializers.product_inventory_serializer import (
    ProductInventorySerializer
)
from users.models import ShippingAddress
from inventory.serializers.shipping_address_serializer import ShippingAddressSerializer
from permissions import custom_permissions
from permissions.assign_permissions import assign_permissions
from rest_framework import permissions
from rest_framework.pagination import PageNumberPagination
from django.db.models import Min, Case, When, Value, Count, F
from rest_framework import status


class Products(ModelViewSet):
    queryset = models.Product.objects.annotate(
        min_price=Min('inventories__sale_price')).order_by('created_at').filter(is_active=True)
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    permission_classes = [custom_permissions.IsAdminOrReadOnly]
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

    ordering = ['-created_at']

    def get_queryset(self):
        request = self.request
        if request.user and request.user.is_authenticated:
            return models.Product.objects.all().annotate(
                is_in_wishlist=Case(
                    When(
                        wishlistitem__wishlist__user=request.user,
                        then=Value(True)
                    ),
                    default=Value(False)
                ),
                min_price=Min('inventories__sale_price')
            ).order_by('created_at').filter(is_active=True)
        else:
            return models.Product.objects.all().annotate(
                min_price=Min('inventories__sale_price')
            ).order_by('created_at').filter(is_active=True)


class ProductInventory(ModelViewSet):
    queryset = models.ProductInventory.objects.filter(is_active=True)
    serializer_class = ProductInventorySerializer
    permission_classes = [custom_permissions.IsAdminOrReadOnly]
    pagination_class = PageNumberPagination
    lookup_field = 'sku'
    # filterset_class = ProductInventoryFilter


class Category(ModelViewSet):
    queryset = models.Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [custom_permissions.IsAdminOrReadOnly]
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
    permission_classes = [custom_permissions.IsAdminOrReadOnly]
    pagination_class = None


class ReviewView(ModelViewSet):
    queryset = models.Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['rating']
    permission_classes = [custom_permissions.IsAuthenticatedAndIsObjectOwner]
    assign_perms = [
        'inventory.change_review',
        'inventory.delete_review',
        'inventory.view_review'
    ]

    def get_serializer_context(self):
        return {
            'user_pk': self.request.user,
            'product_slug': self.kwargs['product_slug']
        }

    def perform_create(self, serializer):
        review = serializer.save()
        assign_permissions(self.request.user, review, self.assign_perms)

    def get_permission_type(self):
        request = self.request
        if request.method == 'PATCH':
            return 'inventory.change_review'
        elif request.method == 'DELETE':
            return 'inventory.delete_review'
        return 'inventory.view_review'


class CartView(
    mixins.ListModelMixin,
    GenericViewSet
):
    # ! prefect product here to prevent multiple queries when serializer is
    # ! summing up the total price in cart
    queryset = models.Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        custom_permissions.CreateForMyAccount
    ]
    pagination_class = None
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        cart, created = self.get_queryset().get_or_create(user=request.user)
        print('HERE', cart)
        serializer = CartSerializer(cart)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class CartItemView(ModelViewSet):

    permission_classes = [permissions.IsAuthenticated]

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
            'cart_pk': self.kwargs['cart_pk']
        }


class ShippingAddressView(ModelViewSet):
    queryset = ShippingAddress.objects.all()
    serializer_class = ShippingAddressSerializer
    permission_classes = [
        custom_permissions.CreateForMyAccount
    ]

    pagination_class = None

    def get_queryset(self):
        # ! filtering based on current user and not user_pk in param because user id is not
        # ! uuidv4 and any id passed in the url param will be returned
        return ShippingAddress.objects.filter(user=self.request.user)


class OrderView(ModelViewSet):
    queryset = models.Order.objects.all()
    permission_classes = [permissions.IsAuthenticated,
                          custom_permissions.CreateForMyAccount]
    http_method_names = ['post', 'get', 'delete']
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
                'user_pk': request.user,
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
        return models.OrderItem.objects.filter(order=self.kwargs['order_pk'], order__user=self.request.user)

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
    permission_classes = [
        permissions.IsAuthenticated,
        custom_permissions.CreateForMyAccount
    ]
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        wishlist, created = models.Wishlist.objects.get_or_create(
            user=request.user)
        serializer = WishlistSerializer(wishlist)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def get_queryset(self):
        return models.Wishlist.objects.filter(user=self.request.user)


class WishlistItemView(ModelViewSet):
    serializer_class = WishlistItemSerializer
    queryset = models.WishlistItem.objects.all().order_by('pk')
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return models.WishlistItem.objects.filter(wishlist=self.kwargs['wishlist_pk'], wishlist__user=self.request.user)

    def get_serializer_context(self):
        return {
            'user_pk': self.request.user
        }

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateWishlistItemSerializer
        else:
            return WishlistItemSerializer

    # def create(self, request, *args, **kwargs):
    #     try:
    #         print('TRY BLOCK')
    #         serializer = CreateWishlistItemSerializer(data=request.data)
    #         serializer.is_valid(raise_exception=True)
    #         wishlist = models.WishlistItem.objects.get(
    #             wishlist=serializer.validated_data['wishlist'],
    #             product=serializer.validated_data['product']
    #         )
    #         wishlist.delete()
    #         return Response(data={}, status=status.HTTP_200_OK)
    #     except models.WishlistItem.DoesNotExist:
    #         print('EXCEPT BLOCK')
    #         wishlist = models.WishlistItem.objects.create(
    #             wishlist=serializer.validated_data['wishlist'],
    #             product=serializer.validated_data['product']
    #         )
    #         wishlist = WishlistItemSerializer(wishlist)
    #         return Response(data=wishlist.data, status=status.HTTP_201_CREATED)


class UserView(mixins.ListModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(pk=user.pk)
