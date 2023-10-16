from django.http import HttpResponse
from django.http import JsonResponse
from utils import get_request_params
from django.contrib.auth.models import User
from common.models import CustomUser
import json
import traceback

"""
此文件仅处理 user表 数据
"""


def dispatcher(request):

    action = request.GET.get('action')
    if action == 'getrank':
        return get_rank(request)
    else:
        return JsonResponse({'ret': 1, 'msg': 'Unsupported request!'})


def get_rank(request):
    if request.method != 'GET':
        return JsonResponse({
            'ret': 'error',
            'msg': 'Unsupported request method.',
        })
    try:
        users = CustomUser.objects.all()
        user_data = []
        for user in users:
            user_data.append({
                'user_id': user.user_id,
                'user_name': user.user.username,
                'score':user.score,
                'last_commit': user.last_answer_time,
            })
        return JsonResponse({'ret': 0, 'retlist': user_data, 'total': len(user_data)})
    except CustomUser.DoesNotExist():
        return JsonResponse({'ret': 'error', 'msg': 'User not found!'})
    except:
        return JsonResponse({'ret': 'error', 'msg': f'未知错误\n{traceback.format_exc()}'})