# Generated by Django 4.1.3 on 2022-12-22 22:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('main', '0010_remove_paymentinformation_ccp_or_rip_not_null'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentinformation',
            name='ccp',
            field=models.CharField(default='0024242424/24', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='paymentinformation',
            name='rip',
            field=models.CharField(default='0079999002453623936', max_length=255, null=True),
        ),
    ]