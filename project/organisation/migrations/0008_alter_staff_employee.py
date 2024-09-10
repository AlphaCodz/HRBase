# Generated by Django 4.2.11 on 2024-09-10 21:34

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('organisation', '0007_alter_staff_employee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='employee',
            field=models.ManyToManyField(limit_choices_to={'role': 'USER'}, related_name='organization_employees', to=settings.AUTH_USER_MODEL),
        ),
    ]
