from django.http import HttpResponse
from django.http import JsonResponse
from common.controller.util import get_request_params
import json

"""
此文件仅处理 user表 数据
"""


def dispatcher(request):
    # 将请求参数统一放入request 的 params 属性中，方便后续处理

    request.params = get_request_params(request)
    """# GET请求 参数在url中，同过request 对象的 GET属性获取
    if request.method == 'GET':
        request.params = request.GET

    # POST/PUT/DELETE 请求 参数 从 request 对象的 body 属性中获取
    elif request.method in ['POST', 'PUT', 'DELETE']:
        # 根据接口，POST/PUT/DELETE 请求的消息体都是 json格式
        request.params = json.loads(request.body)"""

    # 根据不同的action分派给不同的函数进行处理
    action = request.params['action']
    if action == 'userprofile':
        return user_profile(request)
    elif action == 'adduser':
        return add_user(request)
    elif action == 'modifyuser':
        return modify_user(request)
    elif action == 'deluser':
        return del_user(request)

    else:
        return JsonResponse({'ret': 1, 'msg': 'Unsupported request!'})


def user_profile(request):
    """ 读取用户数据，此时计算分数，更新到数据库中 """
    # TODO

    return HttpResponse()


def add_user(request):
    """ 创建新用户 """
    # TODO

    return HttpResponse()


def modify_user(request):
    """ 处理用户更新信息 """
    # TODO

    return HttpResponse()


def del_user(request):
    """ 用户注销账号，删除数据库中与该用户有关的所有数据 """
    # TODO

    return HttpResponse()

