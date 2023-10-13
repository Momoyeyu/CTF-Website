# Generated by Django 4.2.6 on 2023-10-13 11:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_name', models.CharField(max_length=255, unique=True)),
                ('team_member_count', models.IntegerField(default=1)),
                ('allow_join', models.BooleanField(default=True)),
                ('group', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='auth.group')),
                ('leader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_leader', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('user_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='custom_user', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('total_points', models.IntegerField(default=0)),
                ('last_answer_time', models.DateTimeField(blank=True, null=True)),
                ('group_id', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_group', to='auth.group')),
            ],
        ),
    ]
