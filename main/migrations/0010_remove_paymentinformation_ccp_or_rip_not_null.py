# Generated by Django 4.1.3 on 2022-12-21 22:13

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('main', '0009_alter_celebrity_availability'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='paymentinformation',
            name='ccp_or_rip_not_null',
        ),
    ]