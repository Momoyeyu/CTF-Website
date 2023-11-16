from utils import get_request_params, error_template, success_template, ExceptionEnum, SuccessEnum
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
    elif action == "check_messages":
        return check_messages(request)

    else:
        return error_template(ExceptionEnum.UNSUPPORTED_REQUEST.value, status=405)


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
        "data": {
            "message_list": [
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
            ],
            "total": 2,
        }
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
    res_data = {
        "message_list": [],
        "total": 0,
    }
    if not messages:  # 没有查询到消息，但请求是合法的
        return success_template(SuccessEnum.QUERY_SUCCESS.value, data=res_data)

    messages_list = []
    for message in messages:
        if message.receiver is None or message.origin is None:
            message.delete()
            continue
        info = {
            "receiver": message.receiver.username,
            "origin": message.origin.username,
            "message": message.msg,
            "create_time": message.create_time.isoformat()
        }
        messages_list.append(info)
    res_data["message_list"] = messages_list
    res_data["total"] = len(messages_list)
    return success_template(SuccessEnum.QUERY_SUCCESS.value, data=res_data)


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
        "data": {
            "applicant_list": ["aaa", "bbb"],
            "total": 2,
        }
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
    res_data = {
        "applicant_list": [],
        "total": 0,
    }
    if not messages:  # 没有查询到消息，但请求是合法的
        return success_template(SuccessEnum.QUERY_SUCCESS.value, data=res_data)

    applicant_list = []
    for message in messages:
        if message.origin is None:
            message.delete()
            continue
        applicant_list.append(message.origin.username)

    res_data["applicant_list"] = applicant_list
    res_data["total"] = len(applicant_list)
    return success_template(SuccessEnum.QUERY_SUCCESS.value, data=res_data)


def get_invitations(request):
    """
    GET
    @payload:
    {
        "action": "get_invitations",
    }
    @return:
    {
        "ret": "success" / "error",
        "msg": "信息查询成功" / "其他报错",
        "data": {
            "invitation_list": [
                {
                    "inviter": "xx1",
                    "team_name": "EZCTF",
                },
                {
                    "inviter": "xx2",
                    "team_name": "GENSHIN",
                },
            ],
            "total": 2,
        }
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
    #                                                                                 # INVITATION.value = 4
    messages = Message.objects.filter(receiver_id=user.id, msg_type=Message.MessageType.INVITATION.value)

    res_data = {
        "invitation_list": [],
        "total": 0,
    }
    if not messages:  # 没有查询到消息，但请求是合法的
        return success_template(SuccessEnum.QUERY_SUCCESS.value, status=200)

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

    res_data["invitation_list"] = invitation_list
    res_data["total"] = len(invitation_list)
    return success_template(SuccessEnum.QUERY_SUCCESS.value, data=res_data)


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
    if user is None or user.is_active is False:
        return error_template(ExceptionEnum.USER_NOT_FOUND.value, status=404)

    Message.objects.filter(receiver=user).update(checked=True)
    return success_template(SuccessEnum.REQUEST_SUCCESS.value)
