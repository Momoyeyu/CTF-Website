# Generated by Django 4.2.6 on 2023-10-13 11:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rank', '0002_remove_userprofile_rank'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='user',
        ),
        migrations.DeleteModel(
            name='Team',
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]