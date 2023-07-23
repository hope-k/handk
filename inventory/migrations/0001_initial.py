# Generated by Django 4.1.6 on 2023-06-09 22:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
import mptt.fields
import storage.custom_cloudinary_storage
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Brand",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="format: required, max_length=255",
                        max_length=255,
                        unique=True,
                        verbose_name="Brand Name",
                    ),
                ),
            ],
            options={
                "verbose_name": "Brand",
                "verbose_name_plural": "Brands",
            },
        ),
        migrations.CreateModel(
            name="Cart",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                ("created_at", models.DateField(auto_now_add=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="cart",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="format: required, max_length=100",
                        max_length=100,
                        unique=True,
                        verbose_name="Category Name",
                    ),
                ),
                (
                    "slug",
                    django_extensions.db.fields.AutoSlugField(
                        blank=True,
                        editable=False,
                        max_length=150,
                        overwrite=True,
                        populate_from="name",
                        unique=True,
                        verbose_name="Category Slug",
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("lft", models.PositiveIntegerField(editable=False)),
                ("rght", models.PositiveIntegerField(editable=False)),
                ("tree_id", models.PositiveIntegerField(db_index=True, editable=False)),
                ("level", models.PositiveIntegerField(editable=False)),
                (
                    "parent",
                    mptt.fields.TreeForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="children",
                        to="inventory.category",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                ("created_at", models.DateField(auto_now_add=True)),
                ("updated_at", models.DateField(auto_now=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("processing", "Processing"),
                            ("shipped", "shipped"),
                            ("delivered", "Delivered"),
                            ("cancelled", "Cancelled"),
                        ],
                        default="pending",
                        max_length=25,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="order",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "uuid",
                    models.CharField(
                        default=uuid.uuid4,
                        editable=False,
                        help_text="format: required, editable=False",
                        max_length=36,
                        verbose_name="Product UUID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="format: required, max_length=255",
                        max_length=255,
                        verbose_name="Product Name",
                    ),
                ),
                (
                    "slug",
                    django_extensions.db.fields.AutoSlugField(
                        blank=True,
                        editable=False,
                        max_length=150,
                        overwrite=True,
                        populate_from=["name", "uuid"],
                        verbose_name="Product Slug",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        help_text="format: required, max_length=500",
                        max_length=500,
                        verbose_name="Product Description",
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                (
                    "created_at",
                    django_extensions.db.fields.CreationDateTimeField(
                        auto_now_add=True, verbose_name="Product Created At"
                    ),
                ),
                (
                    "updated_at",
                    django_extensions.db.fields.ModificationDateTimeField(
                        auto_now=True, verbose_name="Product Updated At"
                    ),
                ),
                (
                    "brand",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="inventory.brand",
                    ),
                ),
                (
                    "category",
                    mptt.fields.TreeManyToManyField(
                        to="inventory.category", verbose_name="Product Category"
                    ),
                ),
            ],
            options={
                "verbose_name": "Product",
                "verbose_name_plural": "Products",
            },
        ),
        migrations.CreateModel(
            name="ProductAttribute",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="format: required, max_length=255",
                        max_length=255,
                        verbose_name="Product Attribute Name",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        help_text="format: required, max_length=255",
                        max_length=255,
                        verbose_name="Product Attribute Description",
                    ),
                ),
            ],
            options={
                "verbose_name": "Product Attribute",
                "verbose_name_plural": "Product Attributes",
            },
        ),
        migrations.CreateModel(
            name="ProductAttributeValue",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "attribute_value",
                    models.CharField(
                        help_text="format: required, max_length=255",
                        max_length=255,
                        verbose_name="Product Attribute Value",
                    ),
                ),
                (
                    "product_attribute",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="inventory.productattribute",
                    ),
                ),
            ],
            options={
                "verbose_name": "Product Attribute Value",
                "verbose_name_plural": "Product Attribute Values",
            },
        ),
        migrations.CreateModel(
            name="ProductInventory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "sku",
                    models.CharField(
                        blank=True,
                        help_text="format: required, max_length=20",
                        max_length=20,
                        null=True,
                        unique=True,
                        verbose_name="Product Stock Keeping Unit",
                    ),
                ),
                (
                    "upc",
                    models.CharField(
                        blank=True,
                        max_length=12,
                        null=True,
                        unique=True,
                        verbose_name="Universal Product Code",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True, verbose_name="Product Inventory Visibility"
                    ),
                ),
                (
                    "retail_price",
                    models.DecimalField(
                        decimal_places=2,
                        error_messages={
                            "max_digits": "Retail price must be less than 999.99"
                        },
                        help_text="format: required, max_digits=5, decimal_places=2",
                        max_digits=7,
                        verbose_name="Product Retail Price",
                    ),
                ),
                (
                    "store_price",
                    models.DecimalField(
                        decimal_places=2,
                        error_messages={
                            "max_digits": "Store price must be less than 999.99"
                        },
                        help_text="format: required, max_digits=5, decimal_places=2",
                        max_digits=7,
                        verbose_name="Product Store Price",
                    ),
                ),
                (
                    "sale_price",
                    models.DecimalField(
                        decimal_places=2,
                        error_messages={
                            "max_digits": "Store price must be less than 999.99"
                        },
                        help_text="format: required, max_digits=5, decimal_places=2",
                        max_digits=7,
                        verbose_name="Product Sale Price",
                    ),
                ),
                (
                    "is_default",
                    models.BooleanField(
                        default=False, verbose_name="Product Inventory Default"
                    ),
                ),
                (
                    "is_on_sale",
                    models.BooleanField(
                        default=False, verbose_name="Product Inventory On Sale"
                    ),
                ),
                (
                    "created_at",
                    django_extensions.db.fields.CreationDateTimeField(
                        auto_now_add=True, verbose_name="Product Inventory Created At"
                    ),
                ),
                (
                    "updated_at",
                    django_extensions.db.fields.ModificationDateTimeField(
                        auto_now=True, verbose_name="Product Inventory Updated At"
                    ),
                ),
                (
                    "attribute_values",
                    models.ManyToManyField(
                        related_name="attributes",
                        to="inventory.productattributevalue",
                        verbose_name="Product Attribute Values",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="inventories",
                        to="inventory.product",
                    ),
                ),
            ],
            options={
                "verbose_name": "Product Inventory",
                "verbose_name_plural": "Product Inventories",
            },
        ),
        migrations.CreateModel(
            name="ProductType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="format: required, max_length=255",
                        max_length=255,
                        unique=True,
                        verbose_name="Type of Product",
                    ),
                ),
            ],
            options={
                "verbose_name": "Product Type",
                "verbose_name_plural": "Product Types",
            },
        ),
        migrations.CreateModel(
            name="Stock",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "last_checked",
                    models.DateTimeField(verbose_name="Inventory Stock Checked At"),
                ),
                (
                    "units",
                    models.IntegerField(
                        default=0, verbose_name="Inventory Stock Units/Oty"
                    ),
                ),
                (
                    "units_sold",
                    models.IntegerField(default=0, verbose_name="Inventory Stock Sold"),
                ),
                (
                    "product_inventory",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="stock",
                        to="inventory.productinventory",
                    ),
                ),
            ],
            options={
                "verbose_name": "Product Inventory Stock",
                "verbose_name_plural": "Product Inventory Stocks",
            },
        ),
        migrations.CreateModel(
            name="Review",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("comment", models.TextField(max_length=225)),
                ("rating", models.FloatField(max_length=5)),
                ("created_at", models.DateField(auto_now_add=True)),
                ("updated_at", models.DateField(auto_now=True)),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="inventory.product",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="reviews",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Product Review",
                "verbose_name_plural": "Product Reviews",
            },
        ),
        migrations.AddField(
            model_name="product",
            name="product_type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="inventory.producttype"
            ),
        ),
        migrations.CreateModel(
            name="OrderItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quantity", models.PositiveBigIntegerField(default=0)),
                (
                    "unit_price",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=5),
                ),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="order_items",
                        to="inventory.order",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="inventory.productinventory",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Media",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        storage=storage.custom_cloudinary_storage.CustomStorage(),
                        upload_to="product_images",
                        verbose_name="Product Image",
                    ),
                ),
                (
                    "alt_text",
                    models.CharField(
                        blank=True,
                        max_length=255,
                        null=True,
                        verbose_name="Product Image Alt Text",
                    ),
                ),
                (
                    "is_feature",
                    models.BooleanField(default=False, verbose_name="Featured Image"),
                ),
                (
                    "created_at",
                    django_extensions.db.fields.CreationDateTimeField(
                        auto_now_add=True
                    ),
                ),
                (
                    "updated_at",
                    django_extensions.db.fields.ModificationDateTimeField(
                        auto_now=True
                    ),
                ),
                (
                    "product_inventory",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="images",
                        to="inventory.productinventory",
                    ),
                ),
            ],
            options={
                "verbose_name": "Product Image",
                "verbose_name_plural": "Product Images",
            },
        ),
        migrations.CreateModel(
            name="Wishlist",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="inventory.product",
                        verbose_name="Wishlist Product",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="wishlist",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "User Wishlist",
                "unique_together": {("product", "user")},
            },
        ),
        migrations.CreateModel(
            name="CartItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quantity", models.PositiveBigIntegerField(default=0)),
                (
                    "cart",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="cart_items",
                        to="inventory.cart",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="inventory.productinventory",
                    ),
                ),
            ],
            options={
                "unique_together": {("cart", "product")},
            },
        ),
    ]
