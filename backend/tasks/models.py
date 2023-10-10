from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    id = models.AutoField(primary_key=True)  # 自动生成的主键
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 外键关联到auth_user表的id字段
    task_name = models.CharField(max_length=255)  # 题目名称
    content = models.TextField()  # 题目内容描述
    annex = models.CharField(max_length=255)  # 题目附件url
    hint = models.TextField()  # 提示
    flag = models.CharField(max_length=255)  # Flag，需要做好数据保护
    difficulty = models.IntegerField(choices=[(0, 'Easy'), (1, 'Medium'), (2, 'Hard')])  # 题目难度
    points = models.IntegerField()  # 本题分值
    type = models.IntegerField(choices=[(0, 'Misc'), (1, 'Pwn'), (2, 'Web'), (3, 'Reverse'), (4, 'Crypto')])  # 题目类型

    def __str__(self):
        return f"Task ID: {self.id}, Task Name: {self.task_name}, Difficulty: {self.get_difficulty_display()}, Points: {self.points}, Type: {self.get_type_display()}"


class AnswerRecord(models.Model):
    id = models.AutoField(primary_key=True)  # 自动生成的主键
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 外键关联到auth_user表的id字段
    task = models.ForeignKey(Task, on_delete=models.CASCADE)  # 外键关联到tasks_task表的id字段
    points = models.IntegerField()  # 本题得分
    clear_time = models.DateTimeField()  # 用户成功答题时间

    def __str__(self):
        return f"Answer Record ID: {self.id}, User ID: {self.user_id}, Task ID: {self.task_id}, Points: {self.points}, Clear Time: {self.clear_time}"
