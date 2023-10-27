import json
import re
from enum import Enum
from django.http import JsonResponse

from common.models import Message


def get_request_params(request):
    """
    此函数处理不同 HTTP 请求 params 位置不同的问题，返回对应的 params
    经过此函数处理，request.params 里的对象已经转为 python 字典，数据类型也已经经过处理
    @param: request
    @return: request.params
    """
    if request.method == 'GET':
        params = request.GET

    # POST/PUT/DELETE 请求 参数 从 request 对象的 body 属性中获取
    elif request.method in ['POST', 'PUT', 'DELETE']:
        # 根据接口，POST/PUT/DELETE 请求的消息体都是 json格式
        params = json.loads(request.body)

    return params


def log_test(api_name):
    print("[INFO] Testing " + api_name)


def is_valid_username(username):
    # 使用正则表达式检查用户名是否只包含字母、数字和下划线
    pattern = r'^\w+$'
    if re.match(pattern, username):
        return True
    else:
        return False


class ExceptionEnum(Enum):
    INVALID_REQUEST_METHOD = "Invalid Request Method"
    USER_NOT_LOGIN = "用户未登录"
    USER_NOT_FOUND = "未查询到用户"
    TEAM_NOT_FOUND = "未查询到战队"
    MESSAGE_NOT_FOUND = "未查询到信息"
    DATA_NOT_FOUND = "未查询到数据"
    NOT_LEADER = "不是队长，权限不足"
    UNAUTHORIZED = "非授权操作"


def success_template(msg, data=None, status=200):
    if data is None:
        return JsonResponse({
            "ret": "success",
            "msg": msg,
        }, status=status)
    else:
        return JsonResponse({
            "ret": "success",
            "msg": msg,
            "data": data,
        }, status=status)


def error_template(msg, data=None, status=500):
    if data is None:
        return JsonResponse({
            "ret": "error",
            "msg": msg,
        }, status=status)
    else:
        return JsonResponse({
            "ret": "error",
            "msg": msg,
            "data": data
        }, status=status)


def send_message(receiver_id, origin_id, msg, type):
    message = Message(receiver_id=receiver_id, origin_id=origin_id, message=msg, type=type)
    message.check = False
    message.save()
