from django.dispatch import receiver
from django.db.models.signals import post_save
import logging
from django.db import transaction
from .models.primary_models import Organisation
from entity.models.base_models import User

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Organisation)
def update_user_role(sender, instance, created, **kwargs):
    if created:
        admin = instance.admin  # Assuming this is a ForeignKey to User
        if not admin:
            logger.error(f"No admin found for Organisation {instance.id}")
            return
        admin.role = "ORG_ADMIN"
        admin.save()
