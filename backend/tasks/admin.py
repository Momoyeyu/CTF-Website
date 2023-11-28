from django.contrib import admin

# Register your models here.
from tasks.models import Task, AnswerRecord

admin.site.register(Task)
admin.site.register(AnswerRecord)
