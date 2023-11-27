from utils import get_request_params, error_template, success_template, ExceptionEnum, SuccessEnum
from common.models import Message, CustomUser
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.db.models import Q


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
    elif action == "check_message":
        return check_message(request)
    elif action == "get_unchecked_count":
        return get_unchecked_count(request)
    elif action == "check_all":
        return check_all(request)

    else:
        return error_template(ExceptionEnum.UNSUPPORTED_REQUEST.value, status=405)


@login_required
@require_http_methods("GET")
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
                    "msg_type": 3,
                    "checked": false,
                },
                {
                    "receiver": "xx2",
                    "origin": "momoyeyu",
                    "message": "hello",
                    "create_time": "2023-10-27T14:30:00.000Z",
                    "msg_type: 1,
                    "checked": true,
                },
            ],
            "total": 2,
            "unchecked_count": 1,
        }
    }
    """
    if not request.user.is_authenticated:
        return error_template(ExceptionEnum.USER_NOT_LOGIN.value, status=403)

    uid = request.session.get('_auth_user_id')
    user = User.objects.get(pk=uid)
    if user is None:
        return error_template(ExceptionEnum.USER_NOT_FOUND.value, status=404)

    messages = Message.objects.filter((Q(receiver=user) | Q(origin=user)) & Q(is_active=True))
    res_data = {
        "message_list": [],
        "total": 0,
        "unchecked_count": 0,
    }
    if not messages:  # 没有查询到消息，但请求是合法的
        return success_template(SuccessEnum.QUERY_SUCCESS.value, data=res_data)

    messages_list = []
    unchecked_count = 0
    for message in messages:
        if message.receiver is None or message.origin is None:
            message.delete()
            continue
        check_flag = message.checked
        if check_flag is False:
            unchecked_count += 1
        info = {
            "message_id": message.id,
            "receiver": message.receiver.username,
            "origin": message.origin.username,
            "message": message.msg,
            "create_time": message.create_time.isoformat(),
            "msg_type": message.msg_type,
            "checked": check_flag,
        }
        messages_list.append(info)
    res_data = {
        "message_list": messages_list,
        "total": len(messages_list),
        "unchecked_count": unchecked_count,
    }
    return success_template(SuccessEnum.QUERY_SUCCESS.value, data=res_data)


@login_required
@require_http_methods("GET")
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
        "applicant_list": [
            {
                "username": "momoyeyu",
                "score": 100,
            },
            {
                "username": "juanboy",
                "score": 100,
            },
        ],
        "total": 2,
    }
    }
    """
    if not request.user.is_authenticated:
        return error_template(ExceptionEnum.USER_NOT_LOGIN.value, status=403)

    uid = request.session.get('_auth_user_id')
    user = User.objects.get(pk=uid)
    if user is None:
        return error_template(ExceptionEnum.USER_NOT_FOUND.value, status=404)
    #                                                                                 # APPLICATION.value = 3
    messages = Message.objects.filter(receiver_id=user.id,
                                      msg_type=Message.MessageType.APPLICATION.value,
                                      is_active=True)
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
        info = {
            "username": message.origin.username,
            "score": message.origin.custom_user.score,
        }
        applicant_list.append(info)
    res_data = {
        "applicant_list": applicant_list,
        "total": len(applicant_list),
    }
    return success_template(SuccessEnum.QUERY_SUCCESS.value, data=res_data)


@login_required
@require_http_methods("GET")
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
    if not request.user.is_authenticated:
        return error_template(ExceptionEnum.USER_NOT_LOGIN.value, status=403)

    uid = request.session.get('_auth_user_id')
    user = User.objects.get(pk=uid)
    if user is None:
        return error_template(ExceptionEnum.USER_NOT_FOUND.value, status=404)

    messages = Message.objects.filter(receiver_id=user.id,
                                      msg_type=Message.MessageType.INVITATION.value,  # INVITATION.value = 4
                                      is_active=True)
    res_data = {
        "invitation_list": [],
        "total": 0,
    }
    if not messages:  # 没有查询到消息，但请求是合法的
        return success_template(SuccessEnum.QUERY_SUCCESS.value, data=res_data)

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
            "team_name": message.msg,
        }
        invitation_list.append(info)

    res_data["invitation_list"] = invitation_list
    res_data["total"] = len(invitation_list)
    return success_template(SuccessEnum.QUERY_SUCCESS.value, data=res_data)


@login_required
@require_http_methods("GET")
def check_message(request):
    """
    GET
    @param:
    {
        "action": "check_message",
        "message_id": 1,
    }
    """
    if not request.user.is_authenticated:
        return error_template(ExceptionEnum.USER_NOT_LOGIN.value, status=403)
    message_id = request.params["message_id"]
    if not message_id:
        return error_template(ExceptionEnum.MISS_PARAMETER.value, status=400)
    uid = request.session.get('_auth_user_id')
    user = User.objects.get(pk=uid)
    if user is None or user.is_active is False:
        return error_template(ExceptionEnum.USER_NOT_FOUND.value, status=404)

    message = Message.objects.get(pk=message_id)
    if message.receiver != user and message.origin != user:
        return error_template(ExceptionEnum.UNAUTHORIZED.value, status=403)
    message.checked = True
    message.save()
    return success_template(SuccessEnum.REQUEST_SUCCESS.value)


@login_required
@require_http_methods("GET")
def get_unchecked_count(request):
    """
    GET
    @param:
    {
        "action": "get_unchecked_count",
    }
    """
    if not request.user.is_authenticated:
        return error_template(ExceptionEnum.USER_NOT_LOGIN.value, status=403)
    uid = request.session.get('_auth_user_id')
    user = User.objects.get(pk=uid)
    if user is None or user.is_active is False:
        return error_template(ExceptionEnum.USER_NOT_FOUND.value, status=404)
    messages = Message.objects.filter((Q(origin=user) | Q(receiver=user)) & Q(checked=False) & Q(is_active=True))
    res_data = {
        "unchecked_count": len(messages),
    }
    return success_template(SuccessEnum.QUERY_SUCCESS.value, data=res_data)


@login_required
@require_http_methods("GET")
def check_all(request):
    """
    GET
    @param:
    {
        "action": "check_all",
    }
    """
    if not request.user.is_authenticated:
        return error_template(ExceptionEnum.USER_NOT_LOGIN.value, status=403)

    uid = request.session.get('_auth_user_id')
    user = User.objects.get(pk=uid)
    if user is None or user.is_active is False:
        return error_template(ExceptionEnum.USER_NOT_FOUND.value, status=404)

    Message.objects.filter((Q(origin=user) | Q(receiver=user)) & Q(is_active=True)).update(checked=True)
    return success_template(SuccessEnum.REQUEST_SUCCESS.value)
