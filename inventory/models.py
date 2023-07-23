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
from custom_user.models import CustomUser

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
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name='brand')

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
    description = models.TextField(
        max_length=255,
        verbose_name='Product Attribute Description',
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
        on_delete=models.PROTECT
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
        return (f"{self.product_attribute.name} - {self.attribute_value}")


# !  PRODUCT INVENTORY MODEL
class ProductInventory(models.Model):
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

    )
    sale_price = models.DecimalField(
        max_digits=7,
        decimal_places=2,
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
        related_name='attributes'
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

    def __str__(self):
        return (f"{self.product.name} - {self.sku}")

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


class Review(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.DO_NOTHING, related_name='reviews')
    comment = models.TextField(max_length=225)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    rating = models.FloatField(max_length=5)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.user.first_name}"

    class Meta:
        verbose_name = 'Product Review'
        verbose_name_plural = 'Product Reviews'


class Wishlist(models.Model):
    product = models.ForeignKey(
        Product, verbose_name="Wishlist Product", on_delete=models.CASCADE)
    user = models.OneToOneField(
        CustomUser, related_name='wishlist', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'User Wishlist'
        unique_together = ('product', 'user')


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    user = models.OneToOneField(
        CustomUser, related_name='cart', on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(ProductInventory, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=0)

    class Meta:
        # ! unique together making sure there is only one instance of a product in a cart
        # ? there can be one cart with multiple products(unique products)
        unique_together = [['cart', 'product']]


class Order(models.Model):
    ORDER_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),

    )
    id = models.UUIDField(primary_key=True, default=uuid4)
    user = models.ForeignKey(
        CustomUser, related_name='order', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    status = models.CharField(
        choices=ORDER_STATUS_CHOICES, default='pending', max_length=25)

    def __str__(self):
        return f"{self.id} - {self.status}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(ProductInventory, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=0)
    unit_price = models.DecimalField(decimal_places=2, default=0.00, max_digits=5)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
