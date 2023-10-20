# Generated by Django 4.1.6 on 2023-10-16 03:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("inventory", "0007_cartitem_unit_price"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="productfeature",
            name="feature",
        ),
        migrations.RemoveField(
            model_name="productinventory",
            name="feature_values",
        ),
        migrations.AddField(
            model_name="productfeature",
            name="feature_name",
            field=models.CharField(
                blank=True,
                help_text="format: required, max_length=255",
                max_length=255,
                null=True,
                verbose_name="Product Feature",
            ),
        ),
        migrations.AddField(
            model_name="productfeature",
            name="feature_value",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="productinventory",
            name="features",
            field=models.ManyToManyField(
                related_name="inventory_features",
                to="inventory.productfeature",
                verbose_name="Product Features",
            ),
        ),
        migrations.AlterField(
            model_name="productinventory",
            name="sale_price",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                error_messages={"max_digits": "Store price must be less than 999.99"},
                help_text="format: required, max_digits=5, decimal_places=2",
                max_digits=7,
                null=True,
                verbose_name="Product Sale Price",
            ),
        ),
        migrations.DeleteModel(
            name="ProductFeatureValue",
        ),
    ]
