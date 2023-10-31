from django.http import HttpResponse
from django.http import JsonResponse
from utils import get_request_params, error_template, success_template, ExceptionEnum
from django.contrib.auth.models import User
from common.models import CustomUser
import json
import traceback


def dispatcher(request):

    action = request.GET.get('action')
    if action == 'get_rank':
        return get_rank(request)
    else:
        return JsonResponse({'ret': 1, 'msg': 'Unsupported request!'})


def get_rank(request):
    if request.method != 'GET':
        return error_template(ExceptionEnum.INVALID_REQUEST_METHOD, status=405)

    users = CustomUser.objects.all()
    user_data = []
    for user in users:
        user_data.append({
            'user_name': user.user.username,
            'score':user.score,
            'last_commit': user.last_answer_time,
        })
    return JsonResponse({'ret': 'success', 'retlist': user_data, 'total': len(user_data)})
