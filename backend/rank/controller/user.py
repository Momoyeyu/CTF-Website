from django.http import HttpResponse
from django.http import JsonResponse
from utils import get_request_params, error_template, success_template, ExceptionEnum, SuccessEnum
from common.models import CustomUser
import json
import traceback


def dispatcher(request):

    action = request.GET.get('action')
    if action == 'rank':
        return user_rank(request)
    else:
        return error_template(ExceptionEnum.UNSUPPORTED_REQUEST.value, status=405)


def user_rank(request):
    if request.method != 'GET':
        return error_template(ExceptionEnum.INVALID_REQUEST_METHOD.value, status=405)

    users = CustomUser.objects.all()
    user_list = []
    for user in users:
        user_list.append({
            'user_name': user.user.username,
            'score':user.score,
            'last_commit': user.last_answer_time,
        })
    res_data = {
        "team_list": user_list,
        "total": len(user_list),
    }
    return success_template(SuccessEnum.QUERY_SUCCESS.value, data=res_data)
