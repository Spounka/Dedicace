# Generated by Django 4.1.3 on 2023-01-24 21:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('chat', '0003_rename_parties_discussion_members'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatmessageinfo',
            name='discussion',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    related_name='messages', to='chat.discussion'),
        ),
    ]
