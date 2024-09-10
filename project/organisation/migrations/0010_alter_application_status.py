# Generated by Django 4.2.11 on 2024-09-10 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organisation', '0009_alter_staff_organisation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='status',
            field=models.CharField(choices=[('APPROVED', 'Approved'), ('REJECTED', 'Rejected'), ('PENDING', 'Pending')], default='PENDING'),
        ),
    ]
