from django.contrib.auth.models import User
from django.db import models


class Task(models.Model):
    class TaskType(models.IntegerChoices):
        MISC = 0
        CRYPTO = 1
        WEB = 2
        REVERSE = 3
        PWN = 4

    class Difficulty(models.IntegerChoices):
        EAZY = 0
        Medium = 1
        HARD = 2

    task_name = models.CharField(max_length=100)
    content = models.TextField()
    src = models.TextField(blank=True, null=True)
    annex = models.FileField(upload_to='task_annex/', blank=True, null=True)
    hint = models.TextField(blank=True, null=True)
    flag = models.CharField(max_length=100)
    difficulty = models.IntegerField(choices=Difficulty.choices)
    points = models.IntegerField()
    task_type = models.IntegerField(choices=TaskType.choices)
    solve_count = models.IntegerField(default=0)

    objects = models.Manager()

    def __str__(self):
        return f"Task ID: {self.id}, Task Name: {self.task_name}, Difficulty: {self.get_difficulty_display()}, Points: {self.points}, Type: {self.get_task_type_display()}"


class AnswerRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='all_answer')
    task = models.ForeignKey(Task, on_delete=models.PROTECT, related_name='answer_time')
    points = models.IntegerField()
    answer_time = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def __str__(self):
        return f"Answer Record ID: {self.id}, User ID: {self.user_id}, Task ID: {self.task_id}, Points: {self.points}, Clear Time: {self.clear_time}"
