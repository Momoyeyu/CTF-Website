# Generated by Django 4.2.6 on 2023-10-31 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0006_alter_message_msg_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
