# Generated by Django 4.1.1 on 2022-09-30 18:57

import django.contrib.auth.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_user_managers'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='disponibility',
            options={'verbose_name_plural': 'Disponibilities'},
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(default='username', help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username'),
        ),
    ]
