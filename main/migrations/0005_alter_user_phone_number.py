# Generated by Django 4.1.1 on 2022-10-01 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_user_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(default='+213', max_length=15, unique=True),
        ),
    ]