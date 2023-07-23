from typing import Any
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from guardian.admin import GuardedModelAdmin
from guardian.forms import UserObjectPermissionsForm
from django.utils.translation import gettext_lazy as _


from .models import (
    Category,
    Product,
    Brand,
    ProductType,
    ProductAttribute,
    ProductAttributeValue,
    ProductInventory,
    Media,
    Stock,
    Cart,
    CartItem
)
from custom_user.models import ShippingAddress, CustomUser


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'slug',
        'parent',
        'is_active',
    )
    list_filter = ('is_active',)
    search_fields = ('name', 'slug')
    list_display_links = ('id', 'name')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'uuid',
        'name',
        'slug',
        'brand',
        'product_type',
        'description',
        'is_active',
        'created_at',
        'updated_at',
    )
    list_filter = ('is_active', 'created_at', 'updated_at')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ['name']}
    date_hierarchy = 'created_at'
    list_display_links = ('id', 'name')


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    list_display_links = ('id', 'name')


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    list_display_links = ('id', 'name')


@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('name',)
    list_display_links = ('id', 'name')


@admin.register(ProductAttributeValue)
class ProductAttributeValueAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_attribute', 'attribute_value')
    list_filter = ('product_attribute',)
    list_display_links = ('id', 'product_attribute')


@admin.register(ProductInventory)
class ProductInventoryAdmin(admin.ModelAdmin):
    # add delete selected action

    list_display = (
        'id',
        'product',
        'sku',
        'upc',
        'is_active',
        'retail_price',
        'store_price',
        'sale_price',
        'is_default',
        'is_on_sale',
        'created_at',
        'updated_at',
    )
    list_filter = (
        'is_active',
        'is_default',
        'is_on_sale',
        'created_at',
        'updated_at',
    )
    date_hierarchy = 'created_at'
    list_display_links = ('id', 'product')


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'product_inventory',
        'image',
        'alt_text',
        'is_feature',
        'created_at',
        'updated_at',
    )
    list_filter = ('is_feature', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'
    list_display_links = ('id', 'product_inventory')

    # ! using delete_queryset() to delete images from cloudinary because the default delete_queryset() does not delete images from cloudinary
    def delete_queryset(self, request, queryset):
        for obj in queryset.all():
            obj.image.storage.delete(obj.image.name)

        super().delete_queryset(request, queryset)


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'product_inventory',
        'last_checked',
        'units',
        'units_sold',
    )
    list_filter = ('last_checked',)
    list_display_links = ('id', 'product_inventory')


@admin.register(ShippingAddress)
class ShippingAddressAdmin(GuardedModelAdmin):
    list_display = (
        'id',
        'user',
        'street',
        'city',
        'state',
        'zip_code',
        'country',
        'phone_number',
        'is_default',
    )
    list_filter = ('user', 'is_default')


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ("email", "first_name", "last_name", "is_staff", "is_superuser")
    ordering = ["id"]
    list_editable = ('is_staff', 'is_superuser')
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at')
    list_filter = ('user', 'created_at')
    date_hierarchy = 'created_at'


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'product', 'quantity')
    list_filter = ('cart', 'product')
