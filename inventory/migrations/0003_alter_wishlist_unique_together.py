# Generated by Django 4.1.6 on 2023-10-06 21:54

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("inventory", "0002_alter_wishlist_unique_together"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="wishlist",
            unique_together=set(),
        ),
    ]
