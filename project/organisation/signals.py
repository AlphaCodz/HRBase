from django.dispatch import receiver
from django.db.models.signals import post_save
import logging
from django.db import transaction
from .models.primary_models import Organisation, Staff
from entity.models.base_models import User, Role

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Organisation)
def update_user_role(sender, instance, created, **kwargs):
    if created:
        admin = instance.admin
        if admin:
            with transaction.atomic():
                admin.role = "ORG_ADMIN"
                admin.save()

@receiver(post_save, sender=Staff)
def update_employee_roles(sender, instance, created, **kwargs):
    if created:
        employees = instance.employee.all()
        for employee in employees:
            if employee.role != "ORG_STAFF":  # Check if the role needs to be updated
                try:
                    with transaction.atomic():
                        employee.role = "ORG_STAFF"
                        employee.save()
                        logger.debug(f"Updated role for employee {employee.id} to ORG_STAFF")
                except Exception as e:
                    logger.error(f"Error updating role for employee {employee.id}: {e}", exc_info=True)
            else:
                logger.debug(f"Employee {employee.id} already has the role ORG_STAFF")