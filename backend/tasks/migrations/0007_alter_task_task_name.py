# Generated by Django 4.2.6 on 2023-11-28 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0006_rename_type_task_task_type_alter_task_difficulty'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='task_name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]