from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.db import models


class CustomUser(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='custom_user')
    group_id = models.OneToOneField(Group, on_delete=models.CASCADE, null=True, related_name='user_group')
    total_points = models.IntegerField(default=0)
    last_answer_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user_id.username


class Team(models.Model):
    group = models.OneToOneField(Group, on_delete=models.CASCADE)
    team_name = models.CharField(max_length=255, unique=True)
    leader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='team_leader')
    team_member_count = models.IntegerField(default=1)
    allow_join = models.BooleanField(default=True)

    def __str__(self):
        return self.team_name