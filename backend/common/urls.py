from django.urls import path

from common.controller import user, team, message

urlpatterns = [

    path('user', user.dispatcher),
    path('team', team.dispatcher),
    path('message', message.dispatcher),

]
