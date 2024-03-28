from django.urls import path

from rank.controller import user, team

urlpatterns = [

    path('user', user.user_rank),
    path('team', team.team_rank),

]
