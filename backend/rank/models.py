from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_points = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username  # 如果需要，定义用户对象的字符串表示形式


class Team(models.Model):
    group = models.OneToOneField(Group, on_delete=models.CASCADE)
    team_name = models.CharField(max_length=255, unique=True)
    leader = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='team_leader')
    team_member_count = models.IntegerField(default=1)
    allow_join = models.BooleanField(default=True)

    def __str__(self):
        return self.team_name
