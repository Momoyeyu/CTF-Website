from django.urls import path

# import tasks.controller

from tasks.controller import task, answer


urlpatterns = [

    # 用户行为
    path('answer', answer.dispatcher),
    path('list',task.dispatcher),

    # 管理员行为
    # path('add', task.dispatcher),
    # path('del', task.dispatcher),
]
