from django.urls import path

from common.controller import user, team

urlpatterns = [

    path('user', user.dispatcher),
    path('team', team.dispatcher),

]
