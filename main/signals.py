from django.db.models.signals import post_save
from django.dispatch import receiver

import main.models


@receiver(post_save, sender=main.models.User)
def create_payment(sender, instance: main.models.User, created, **kwargs):
    if created and instance.payment_details is None:
        main.models.PaymentInformation.objects.create(user=instance)
