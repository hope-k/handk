from uuid import uuid4
from django.db import models
from django_extensions.db.fields import (
    AutoSlugField,
    CreationDateTimeField,
    ModificationDateTimeField
)
from mptt.models import (
    MPTTModel,
    TreeForeignKey,
    TreeManyToManyField,
)

from storage.custom_cloudinary_storage import CustomStorage
from utils.generate_sku import generate_sku
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

# !  CATEGORY MODEL


class Category(MPTTModel):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Category Name',
        help_text="format: required, max_length=100"
    )
    slug = AutoSlugField(
        populate_from='name',
        unique=True,
        max_length=150,
        verbose_name='Category Slug',
        overwrite=True,
        editable=True
    )
    parent = TreeForeignKey(
        'self',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='children',
    )
    is_active = models.BooleanField(default=True)

    class MPTTMeta:
        order_insertion_by = ['name']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


# ! PRODUCT TYPE MODEL
class ProductType(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Type of Product',
        help_text="format: required, max_length=255"
    )

    class Meta:
        verbose_name = 'Product Type'
        verbose_name_plural = 'Product Types'

    def __str__(self):
        return self.name


# !  BRAND MODEL
class Brand(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Brand Name',
        help_text="format: required, max_length=255"
    )

    class Meta:
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'

    def __str__(self):
        return self.name


# !  PRODUCT MODEL
class Product(models.Model):
    uuid = models.CharField(
        default=uuid4,
        max_length=36,
        editable=False,
        verbose_name='Product UUID',
        help_text="format: required, editable=False"
    )
    name = models.CharField(
        max_length=255,
        unique=False,
        verbose_name='Product Name',
        help_text="format: required, max_length=255"
    )
    product_type = models.ForeignKey(
        ProductType,
        on_delete=models.PROTECT
    )
    brand = models.ForeignKey(
        Brand, on_delete=models.PROTECT, related_name='brand')

    slug = AutoSlugField(
        populate_from=['name', 'uuid'],
        max_length=150,
        verbose_name='Product Slug',
        overwrite=True,
        editable=True
    )
    description = models.TextField(
        max_length=500,
        verbose_name='Product Description',
        help_text="format: required, max_length=500"
    )
    category = TreeManyToManyField(
        Category,
        verbose_name='Product Category',
    )
    is_active = models.BooleanField(default=True)
    created_at = CreationDateTimeField(
        verbose_name='Product Created At'
    )
    updated_at = ModificationDateTimeField(
        verbose_name='Product Updated At'
    )
    features = models.ManyToManyField(
        'ProductFeature',
        verbose_name='Product Features',
        related_name='inventory_features',

    )

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name


class ProductAttribute(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Product Attribute Name',
        help_text="format: required, max_length=255"
    )

    class Meta:
        verbose_name = 'Product Attribute'
        verbose_name_plural = 'Product Attributes'

    def __str__(self):
        return self.name


# ! PRODUCT ATTRIBUTE VALUE MODEL
class ProductAttributeValue(models.Model):
    product_attribute = models.ForeignKey(
        ProductAttribute,
        on_delete=models.CASCADE
    )
    description = models.TextField(
        max_length=255,
        verbose_name='Product Attribute Value Description',
        help_text="format: required, max_length=255",
        null=True,
        blank=True
    )
    attribute_value = models.CharField(
        max_length=255,
        verbose_name='Product Attribute Value',
        help_text="format: required, max_length=255"
    )

    class Meta:
        verbose_name = 'Product Attribute Value'
        verbose_name_plural = 'Product Attribute Values'

    def __str__(self):
        return (f"{self.product_attribute.name} - {self.description} -  {self.attribute_value}")


class ProductFeature(models.Model):
    feature_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='Product Feature',
        help_text="format: required, max_length=255"
    )
    feature_value = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'Product Feature'
        verbose_name_plural = 'Product Features'

    def __str__(self):
        return f"{self.feature_name} - {self.feature_value}"


# !  PRODUCT INVENTORY MODEL
class ProductInventory(models.Model):
    # ! one product has many  ProductInventory ->  []
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='inventories'
    )
    sku = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Product Stock Keeping Unit',
        help_text="format: required, max_length=20",
        null=True,
        blank=True,
    )
    upc = models.CharField(
        max_length=12,
        unique=True,
        verbose_name='Universal Product Code',
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Product Inventory Visibility'
    )
    retail_price = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        verbose_name='Product Retail Price',
        help_text="format: required, max_digits=5, decimal_places=2",
        error_messages={
            'max_digits': 'Retail price must be less than 999.99',
        }

    )
    store_price = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        verbose_name='Product Store Price',
        help_text="format: required, max_digits=5, decimal_places=2",
        error_messages={
            'max_digits': 'Store price must be less than 999.99',
        }

    )  # todo get rid of store price
    sale_price = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Product Sale Price',
        help_text="format: required, max_digits=5, decimal_places=2",
        error_messages={
            'max_digits': 'Store price must be less than 999.99',
        }

    )
    is_default = models.BooleanField(
        default=False,
        verbose_name='Product Inventory Default'
    )
    is_on_sale = models.BooleanField(
        default=False,
        verbose_name='Product Inventory On Sale'
    )
    attribute_values = models.ManyToManyField(
        ProductAttributeValue,
        verbose_name='Product Attribute Values',
        related_name='inventory_attributes',

    )

    created_at = CreationDateTimeField(
        verbose_name='Product Inventory Created At'
    )
    updated_at = ModificationDateTimeField(
        verbose_name='Product Inventory Updated At'
    )

    class Meta:
        verbose_name = 'Product Inventory'
        verbose_name_plural = 'Product Inventories'
        ordering = ['-id']

    def __str__(self):
        return (f"{self.product.name} - {self.pk}")

    def save(self, *args, **kwargs):
        is_new_instance = self.pk is None
        super().save(*args, **kwargs)
        if is_new_instance:  # only generate sku for new instances
            self.sku = generate_sku(pk=self.pk)
        super().save(*args, **kwargs)


# ! MEDIA MODEL

class Media(models.Model):
    product_inventory = models.ForeignKey(
        ProductInventory,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(
        upload_to='product_images',
        verbose_name='Product Image',
        storage=CustomStorage()
    )
    alt_text = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='Product Image Alt Text',
    )
    is_feature = models.BooleanField(
        default=False,
        verbose_name='Featured Image'
    )
    created_at = CreationDateTimeField()
    updated_at = ModificationDateTimeField()

    class Meta:
        verbose_name = 'Product Image'
        verbose_name_plural = 'Product Images'

    def __str__(self):
        return self.product_inventory.product.name

    def delete(self, *args, **kwargs):
        # Delete the image from Cloudinary
        if self.image:
            self.image.storage.delete(self.image.name)

        # Call the parent class's delete() method
        super().delete(*args, **kwargs)


# !  STOCK MODEL
class Stock(models.Model):
    product_inventory = models.OneToOneField(
        ProductInventory,
        on_delete=models.CASCADE,
        related_name='stock'
    )
    last_checked = models.DateTimeField(
        verbose_name='Inventory Stock Checked At',
    )
    units = models.IntegerField(
        verbose_name='Inventory Stock Units/Oty',
        default=0
    )
    units_sold = models.IntegerField(
        verbose_name='Inventory Stock Sold',
        default=0
    )

    class Meta:
        verbose_name = 'Product Inventory Stock'
        verbose_name_plural = 'Product Inventory Stocks'

    def __str__(self):
        return self.product_inventory.product.name


# def validate_rating(value):
#     if value < 1 or value > 5:
#         raise ValidationError('Rating should be between 1 and 5')


class Review(models.Model):
    user = models.ForeignKey(
        get_user_model(), on_delete=models.DO_NOTHING, related_name='reviews')
    comment = models.TextField(max_length=225)
    product = models.ForeignKey(
        Product, on_delete=models.DO_NOTHING, related_name='reviews')
    rating = models.PositiveIntegerField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.user.first_name}"

    def clean(self):

        rating = self.rating

        # Check if rating is less than 1 or greater than 5
        if rating < 1 or rating > 5:
            raise ValidationError('Rating must be between 1 and 5.')

        super().clean()

    class Meta:
        verbose_name = 'Product Review'
        verbose_name_plural = 'Product Reviews'


class Wishlist(models.Model):
    user = models.OneToOneField(
        get_user_model(), related_name='wishlist', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'User Wishlist'

    def __str__(self):
        return f"{self.user.email} Wishlist-{self.pk}"


class WishlistItem(models.Model):
    product = models.ForeignKey(
        Product, verbose_name="Wishlist Product", on_delete=models.CASCADE, related_name='wishlistitem')
    wishlist = models.ForeignKey(
        Wishlist, on_delete=models.CASCADE, related_name='wishlist_items')

    class Meta:
        verbose_name = 'Wishlist Item'
        unique_together = ('product', 'wishlist')

    def __str__(self) -> str:
        return f"{self.wishlist.user.email}-{self.product.name}"


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    user = models.OneToOneField(
        get_user_model(), related_name='cart', on_delete=models.CASCADE, unique=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} - {self.user.email}"


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name='cart_items')
    product_inventory = models.ForeignKey(
        ProductInventory, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveBigIntegerField(default=1)
    unit_price = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        default=0.00,
        verbose_name='Cart unit price',
        help_text="format: required, max_digits=5, decimal_places=2",
        error_messages={
            'max_digits': 'Retail price must be less than 999.99',
        }

    )
    attribute_values = models.ManyToManyField(
        ProductAttributeValue,
        verbose_name='Cart Item Attributes',
        related_name='cart_item_attributes'

    )

    # ? the flow is for user to give the selected inventory with attributes

    class Meta:
        # ! unique together making sure there is only one instance of a product in a cart
        # ? there can be one cart with multiple products(unique products)
        # ? the order matters here

        ordering = ['-id']

    def __str__(self):
        return f"{self.product_inventory.product.name} x {self.quantity}: GHS {self.unit_price}"


class Order(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(
        get_user_model(), related_name='orders', on_delete=models.SET_NULL, null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.id}"


class OrderItem(models.Model):
    ORDER_ITEM_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),

    )
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(
        ProductInventory, on_delete=models.SET_NULL, null=True)
    status = models.CharField(
        choices=ORDER_ITEM_STATUS_CHOICES,
        max_length=25,
        default='pending'
    )
    attribute_values = models.ManyToManyField(
        ProductAttributeValue,
        verbose_name='Order Item Attributes',
        related_name='order_item_attributes',
    )
    quantity = models.PositiveBigIntegerField(default=0)
    unit_price = models.DecimalField(
        decimal_places=2, default=0.00, max_digits=7)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
