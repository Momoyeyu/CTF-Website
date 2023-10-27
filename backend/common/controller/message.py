from django.http import JsonResponse
from utils import get_request_params
from common.models import Message
from django.contrib.auth.models import User


def dispatcher(request):
    # 将请求参数统一放入request 的 params 属性中，方便后续处理

    # 经过此函数处理，request.params 里的对象已经转为 python 字典，数据类型也已经经过处理
    request.params = get_request_params(request)

    # 根据不同的action分派给不同的函数进行处理
    action = request.params["action"]
    if action == "get_message":
        return get_message(request)

    else:
        return JsonResponse({
            "ret": "error",
            "msg": "Unsupported request!"
        }, status=404)


def get_message(request):
    """
    GET
    @payload:
    {
        "action": "create_team",
        "username": "momoyeyu",
    }
    @return:
    {
        "ret": "success" / "error",
        "msg": "信息查询成功" / "其他报错"
    }
    """
    if request.method != "GET":
        return JsonResponse({
            "ret": "error",
            "msg": "Invalid request method"
        }, status=405)

    if not request.user.is_authenticated:
        return JsonResponse({
            "ret": "error",
            "msg": "用户未登录",
        }, status=403)
    data = request.params["data"]
    username = data["username"]

    user = User.objects.get_by_natural_key(username)

    if user is None:
        return JsonResponse({
            "ret": "error",
            "msg": "用户查询失败",
        }, status=404)

    messages = Message.objects.filter(user_id=user.id)

    if messages is None:
        return JsonResponse({
            "ret": "success",
            "msg": "信息查询成功，信息为空",
        }, status=200)

    messages_list = []
    for message in messages:
        info = {
            "from": message.origin.username,
            "to": username,
            "message": message.message,
        }
        messages_list.append(info)

    return JsonResponse({
        "ret": "success",
        "msg": "信息查询成功",
        "data": messages_list,
    }, status=200)


