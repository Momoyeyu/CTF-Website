from django.http import HttpResponse
from django.http import JsonResponse
from common.controller.util import get_request_params
import json


def dispatcher(request):
    # 将请求参数统一放入request 的 params 属性中，方便后续处理

    request.params = get_request_params(request)

    # 根据不同的action分派给不同的函数进行处理
    action = request.params['action']
    if action == 'createteam':
        return create_team(request)
    elif action == 'delteam':
        return del_team(request)
    elif action == 'jointeam':
        return join_team(request)
    elif action == 'quitteam':
        return quit_team(request)

    else:
        return JsonResponse({'ret': 1, 'msg': 'Unsupported request!'})


def create_team(request):

    return HttpResponse()


def del_team(request):

    return HttpResponse()


def join_team(request):
    """ 用户加入队伍 """
    # TODO

    return HttpResponse()


def quit_team(request):

    return HttpResponse()

