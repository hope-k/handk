# Generated by Django 4.1.6 on 2023-10-13 02:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("inventory", "0005_alter_wishlistitem_unique_together"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="cartitem",
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name="wishlistitem",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="wishlistitem",
                to="inventory.product",
                verbose_name="Wishlist Product",
            ),
        ),
    ]
