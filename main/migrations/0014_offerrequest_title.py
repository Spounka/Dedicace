# Generated by Django 4.1.3 on 2023-01-21 21:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_alter_payment_payment_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='offerrequest',
            name='title',
            field=models.CharField(default='Title', max_length=100),
        ),
    ]
