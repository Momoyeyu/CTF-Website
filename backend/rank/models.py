from django.contrib.auth.models import User
from tasks.models import Task
from django.db import models


class FirstKill(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    task = models.ForeignKey(Task, on_delete=models.PROTECT)
    answer_time = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    def __str__(self):
        return f"First Kill: {self.user.username} - {self.task.task_name}"