from django.http import HttpResponse
from django.http import JsonResponse
from utils import get_request_params
from common.models import Team, CustomUser
import json
import traceback


def dispatcher(request):
    action = request.GET.get('action')
    if action == 'getrank':
        return get_rank(request)
    else:
        return JsonResponse({'ret': 'error', 'msg': 'Unsupported request!'})


def get_rank(request):
    if request.method != 'GET':
        return JsonResponse({
            'ret': 'error',
            'msg': 'Unsupported request method.',
        })
    try:
        team_data = []
        teams = Team.objects.all()
        for team in teams:
            members = team.user_group.all()
            total_score = 0
            for member in members:
                total_score += member.score
            team_data.append({
                'team_name': team.team_name,
                'score': total_score,
                'member_count': team.member_count,
            })
            return JsonResponse({'ret': 0, 'retlist': team_data, 'total': len(team_data)})
    except Team.DoesNotExist():
        return JsonResponse({'ret': 'error', 'msg': 'Team not found!'})
    except:
        return JsonResponse({'ret': 'error', 'msg': f'未知错误\n{traceback.format_exc()}'})
