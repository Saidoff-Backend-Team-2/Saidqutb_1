from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
from .utils import generate_order_number
from django.db import IntegrityError

@receiver(post_save, sender=Order)
def create_order_number(sender, instance, created, **kwargs):
    if created and not instance.number:
        try:
            instance.number = generate_order_number()
            instance.save()
        except IntegrityError:
            instance.number = f"#{instance.id:06d}"
            instance.save()