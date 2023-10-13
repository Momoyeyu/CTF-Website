from django.contrib.auth.models import User
from django.db import models


class Task(models.Model):
    TYPE_CHOICES = (
        (0, 'Misc'),
        (1, 'Pwn'),
        (2, 'Web'),
        (3, 'Reverse'),
        (4, 'Crypto'),
    )

    DIFFICULTY_CHOICES = (
        (0, 'Easy'),
        (1, 'Medium'),
        (2, 'Hard'),
    )

    task_name = models.CharField(max_length=100)
    content = models.TextField()
    annex = models.FileField(upload_to='task_annex/', blank=True, null=True)
    hint = models.TextField(blank=True, null=True)
    flag = models.CharField(max_length=100)  # You may want to encrypt the flag.
    difficulty = models.IntegerField(choices=DIFFICULTY_CHOICES)
    points = models.IntegerField()
    type = models.IntegerField(choices=TYPE_CHOICES)
    solve_count = models.IntegerField(default=0)

    def __str__(self):
        return f"Task ID: {self.id}, Task Name: {self.task_name}, Difficulty: {self.get_difficulty_display()}, Points: {self.points}, Type: {self.get_type_display()}"


class AnswerRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    task = models.ForeignKey(Task, on_delete=models.PROTECT)
    points = models.IntegerField()
    answer_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Answer Record ID: {self.id}, User ID: {self.user_id}, Task ID: {self.task_id}, Points: {self.points}, Clear Time: {self.clear_time}"
