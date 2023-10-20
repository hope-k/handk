from django.dispatch import receiver
from django.db.models.signals import post_save
from inventory.models import OrderItem


@receiver(post_save, sender=OrderItem)
def order_cancelled_signal(sender, instance,  **kwargs):
    if instance.status == 'cancelled':
        print(f'=======================>>>>ORDER {instance.pk} CANCELLED')
