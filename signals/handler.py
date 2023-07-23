from django.dispatch import receiver
from django.db.models.signals import post_save
from inventory.models import Order


@receiver(post_save, sender=Order)
def order_cancelled_signal(sender, instance,  **kwargs):
    if instance.status == 'cancelled':
        print(f'=======================>>>>ORDER {instance.pk} CANCELLED')
