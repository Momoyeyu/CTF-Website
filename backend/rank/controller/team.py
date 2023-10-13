from django.http import HttpResponse
from django.http import JsonResponse
from common.controller.util import get_request_params
import json


def dispatcher(request):
    # 将请求参数统一放入request 的 params 属性中，方便后续处理

    request.params = get_request_params(request)

    # 根据不同的action分派给不同的函数进行处理
    action = request.params['action']
    if action == 'getrank':
        return get_rank(request)

    else:
        return JsonResponse({'ret': 1, 'msg': 'Unsupported request!'})


def get_rank(request):

    return HttpResponse()
