# Generated by Django 4.1.6 on 2023-10-16 18:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("inventory", "0008_remove_productfeature_feature_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="productinventory",
            name="features",
        ),
        migrations.AddField(
            model_name="product",
            name="features",
            field=models.ManyToManyField(
                related_name="inventory_features",
                to="inventory.productfeature",
                verbose_name="Product Features",
            ),
        ),
    ]
