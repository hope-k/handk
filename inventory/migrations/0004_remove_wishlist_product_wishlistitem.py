# Generated by Django 4.1.6 on 2023-10-06 21:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("inventory", "0003_alter_wishlist_unique_together"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="wishlist",
            name="product",
        ),
        migrations.CreateModel(
            name="WishlistItem",
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
                    "wishlist",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="wishlist_items",
                        to="inventory.wishlist",
                    ),
                ),
            ],
            options={
                "verbose_name": "Wishlist Item",
            },
        ),
    ]
