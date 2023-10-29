from django.http import JsonResponse
from utils import get_request_params, error_template, success_template, ExceptionEnum
from common.models import Message, CustomUser
from django.contrib.auth.models import User


def dispatcher(request):
    # 将请求参数统一放入request 的 params 属性中，方便后续处理

    # 经过此函数处理，request.params 里的对象已经转为 python 字典，数据类型也已经经过处理
    request.params = get_request_params(request)

    # 根据不同的action分派给不同的函数进行处理
    action = request.params["action"]
    if action == "get_messages":
        return get_messages(request)
    elif action == "get_applications":
        return get_applications(request)
    elif action == "get_invitations":
        return get_invitations(request)

    else:
        return JsonResponse({
            "ret": "error",
            "msg": "Unsupported request!"
        }, status=404)


def get_messages(request):
    """
    GET
    @params:
    {
        "action": "get_message",
    }
    @return:
    {
        "ret": "success" / "error",
        "msg": "信息查询成功" / "其他报错",
        "data": [
            {
                "receiver": "momoyeyu",
                "origin": "xx1",
                "message": "want to join your team"
                "create_time": "2023-10-27T14:30:00.000Z",
            },
            {
                "receiver": "xx2",
                "origin": "momoyeyu",
                "message": "hello",
                "create_time": "2023-10-27T14:30:00.000Z",
            },
        ]
    }
    """
    if request.method != "GET":
        return error_template(ExceptionEnum.INVALID_REQUEST_METHOD.value, status=405)
    if not request.user.is_authenticated:
        return error_template(ExceptionEnum.USER_NOT_LOGIN.value, status=403)

    uid = request.session.get('_auth_user_id')
    user = User.objects.get(pk=uid)
    if user is None:
        return error_template(ExceptionEnum.USER_NOT_FOUND.value, status=404)

    messages = Message.objects.filter(receiver=user) | Message.objects.filter(origin=user)
    if not messages:  # 没有查询到消息，但请求是合法的
        return success_template("信息查询成功，信息为空", status=200)

    messages_list = []
    for message in messages:
        info = {
            "receiver": message.receiver.username,
            "origin": message.origin.username,
            "message": message.msg,
            "create_time": message.create_time.isoformat()
        }
        messages_list.append(info)
    return success_template("信息查询成功", data=messages_list)


def get_applications(request):
    """
    GET
    @params:
    {
        "action": "get_applications",
    }
    @return:
    {
        "ret": "success" / "error",
        "msg": "信息查询成功" / "其他报错",
        "data": [
            {
                "applicant": "xx1",
            },
            {
                "applicant": "xx2",
            },
        ]
    }
    """
    if request.method != "GET":
        return error_template(ExceptionEnum.INVALID_REQUEST_METHOD.value, status=405)
    if not request.user.is_authenticated:
        return error_template(ExceptionEnum.USER_NOT_LOGIN.value, status=403)

    uid = request.session.get('_auth_user_id')
    user = User.objects.get(pk=uid)
    if user is None:
        return error_template(ExceptionEnum.USER_NOT_FOUND.value, status=404)
    #                                                                                 # APPLICATION.value = 3
    messages = Message.objects.filter(receiver_id=user.id, msg_type=Message.MessageType.APPLICATION.value)
    if not messages:  # 没有查询到消息，但请求是合法的
        return success_template("信息查询成功，信息为空", status=200)

    applicant_list = []
    for message in messages:
        info = {
            "applicant": message.origin.username,
        }
        applicant_list.append(info)

    return success_template("信息查询成功", data=applicant_list, status=200)


def get_invitations(request):
    """
    GET
    @payload:
    {
        "action": "get_invitations",
        "username": "momoyeyu",
    }
    @return:
    {
        "ret": "success" / "error",
        "msg": "信息查询成功" / "其他报错",
        "data": [
            {
                "inviter": "xx1",
                "team_name": "EZCTF",
            },
            {
                "inviter": "xx2",
                "team_name": "GENSHIN",
            },
        ]
    }
    """
    if request.method != "GET":
        return error_template(ExceptionEnum.INVALID_REQUEST_METHOD.value, status=405)
    if not request.user.is_authenticated:
        return error_template(ExceptionEnum.USER_NOT_LOGIN.value, status=403)

    username = request.GET.get("username")

    # 接收者
    user = User.objects.get_by_natural_key(username)

    if user is None:
        return error_template(ExceptionEnum.USER_NOT_FOUND.value, status=404)
    #                                                                                 # INVITATION.value = 4
    messages = Message.objects.filter(receiver_id=user.id, msg_type=Message.MessageType.INVITATION.value)

    if not messages:  # 没有查询到消息，但请求是合法的
        return success_template("信息查询成功，信息为空", status=200)

    invitation_list = []
    for message in messages:
        user = User.objects.get_by_natural_key(message.origin.username)
        if user is None or user.is_active is False:
            message.delete()
            continue
        custom_user = CustomUser.objects.get(user=user)
        if custom_user.team is None:
            message.delete()
            continue
        info = {
            "inviter": user.username,
            "team_name": custom_user.team.team_name,
        }
        invitation_list.append(info)

    return success_template("信息查询成功", data=invitation_list, status=200)


def check_messages(request):
    """
    PUT
    @param:
    {
        "action": "check_messages",
    }
    """
    if request.method != "PUT":
        return error_template(ExceptionEnum.INVALID_REQUEST_METHOD.value, status=405)
    if not request.user.is_authenticated:
        return error_template(ExceptionEnum.USER_NOT_LOGIN.value, status=403)
    uid = request.session.get('_auth_user_id')
    user = User.objects.get(pk=uid)
    if user is None:
        return error_template(ExceptionEnum.USER_NOT_FOUND.value, status=404)
