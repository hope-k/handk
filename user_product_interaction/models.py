from django.db import models
from django.contrib.auth import get_user_model
from inventory.models import Product


# Create your models here.
class UserProductInteraction(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING, related_name='interations')
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    duration = models.IntegerField(default=0)

    class Meta:
        unique_together = [['user', 'product']]
