from django.contrib.auth.models import User
from django.db import models

"""
related_name 在Django的模型中用于指定反向关联名称，它对于创建更直观的关联查询和可读性非常有用。
当你在一个模型中定义外键或多对多字段时，Django会自动生成一个默认的反向关联名称，
通常是小写的模型名加 _set，例如 modelname_set
使用 related_name 可以自定义反向关联的名称，这对于让你的代码更易于理解和维护很重要。

# 假设有如下 models
class Comment(models.Model):
    text = models.TextField()
    user = models.ForeignKey(User, related_name='comments')

class Post(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, related_name='posts')

# 查询数据
user = User.objects.get(pk=1)
comments = user.comments.all()  # 使用 related_name，更容易理解
posts = user.posts.all()

"""


class Team(models.Model):
    team_name = models.CharField(max_length=255, unique=True)
    leader = models.ForeignKey(User, on_delete=models.PROTECT, related_name='leader')
    member_count = models.IntegerField(default=1)
    allow_join = models.BooleanField(default=True)
    create_time = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def __str__(self):
        return self.team_name


class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='custom_user')
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='user_group')
    score = models.IntegerField(default=0)
    last_answer_time = models.DateTimeField(null=True, blank=True)

    objects = models.Manager()

    def __str__(self):
        return self.user.username


class Message(models.Model):
    class MessageType(models.IntegerChoices):
        OTHER = 0
        CHAT = 1
        SYSTEM = 2
        APPLICATION = 3
        INVITATION = 4

    # receiver: 接收者
    # origin: 发送者
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    origin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    msg = models.TextField()
    checked = models.BooleanField(default=False)
    msg_type = models.IntegerField(choices=MessageType.choices)
    create_time = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()
