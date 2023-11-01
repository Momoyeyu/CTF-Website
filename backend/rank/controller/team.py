from django.http import HttpResponse
from django.http import JsonResponse
from utils import get_request_params, error_template, success_template, ExceptionEnum, SuccessEnum
from common.models import Team, CustomUser
import json
import traceback


def dispatcher(request):
    action = request.GET.get('action')
    if action == 'rank':
        return team_rank(request)
    else:
        return error_template(ExceptionEnum.UNSUPPORTED_REQUEST.value, status=405)


def team_rank(request):
    """
    @return:
    {
        "ret": "success",
        "msg": "查询成功",
        "data": {
            "team_list": [
                {
                    "team_name": "aaa",
                    "score": 100,
                    "member_count": 2,
                },
                {
                    "username": "bbb",
                    "score": 100,
                    "member_count": 2,
                },
            ],
            "total": 2,
        }
    }
    """
    if request.method != 'GET':
        return error_template(ExceptionEnum.INVALID_REQUEST_METHOD.value, status=405)

    team_list = []
    teams = Team.objects.all()
    for team in teams:
        members = team.user_group.all()
        total_score = 0
        for member in members:
            total_score += member.score
        team_list.append({
            'team_name': team.team_name,
            'score': total_score,
            'member_count': team.member_count,
        })
    res_data = {
        "team_list": team_list,
        "total": len(team_list),
    }
    return success_template(SuccessEnum.QUERY_SUCCESS.value, data=res_data)


