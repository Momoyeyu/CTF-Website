from django.http import HttpResponse
from django.http import JsonResponse
from utils import get_request_params, error_template, success_template, ExceptionEnum, SuccessEnum
from common.models import Team, CustomUser
import json
import traceback


def dispatcher(request):
    action = request.GET.get('action')
    if action == 'get_rank':
        return get_rank(request)
    else:
        return JsonResponse({'ret': 'error', 'msg': 'Unsupported request!'})


def get_rank(request):
    if request.method != 'GET':
        return error_template(ExceptionEnum.INVALID_REQUEST_METHOD, status=405)

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
    return success_template(SuccessEnum.QUERY_SUCCESS, data=res_data, status=405)


