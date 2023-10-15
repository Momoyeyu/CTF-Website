from django.urls import path

import tasks.controller.task

# from tasks.controller import task, answer


urlpatterns = [

    # 用户行为
#    path('answer', tasks.controller.answer.dispatcher),
    path('list',tasks.controller.task.dispatcher),

    # 管理员行为
    # path('add', task.dispatcher),
    # path('del', task.dispatcher),
]
