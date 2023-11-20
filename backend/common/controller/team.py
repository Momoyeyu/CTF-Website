from django.contrib.auth import authenticate
from utils import get_request_params
from common.models import Team, Message, CustomUser
from django.contrib.auth.models import User
from utils import ExceptionEnum, error_template, success_template, send_message, SuccessEnum
from django.contrib.auth.decorators import login_required


def dispatcher(request):
    # 将请求参数统一放入request 的 params 属性中，方便后续处理

    # 经过此函数处理，request.params 里的对象已经转为 python 字典，数据类型也已经经过处理
    request.params = get_request_params(request)
    # 根据不同的action分派给不同的函数进行处理
    action = request.params["action"]

    if not action:
        return error_template(ExceptionEnum.MISS_PARAMETER.value, status=400)

    if action == "create_team":
        return create_team(request)
    elif action == "del_team":
        return del_team(request)
    elif action == "join_team":
        return join_team(request)
    elif action == "quit_team":
        return quit_team(request)
    elif action == "search_team":
        return search_team(request)
    elif action == "change_team_name":
        return change_team_name(request)
    elif action == "change_team_leader":
        return change_team_leader(request)
    elif action == "verify_apply":
        return verify_apply(request)
    elif action == "invite":
        return invite(request)
    elif action == "accept":
        return accept(request)
    elif action == "kick_out":
        return kick_out(request)

    else:
        return error_template(ExceptionEnum.UNSUPPORTED_REQUEST.value, status=405)


@login_required
def create_team(request):
    """
    队长创建战队
    POST 获取数据样例：
    {
        "action": "create_team",
        "data": {
            "team_name": "ezctf",
            "allow_join": "true"
        }
    }
    """
    if request.method != "POST":
        return error_template(ExceptionEnum.INVALID_REQUEST_METHOD.value, status=405)

    if not request.user.is_authenticated:
        return error_template(ExceptionEnum.USER_NOT_LOGIN.value, status=403)
    data = request.params["data"]
    uid = request.session.get('_auth_user_id')
    if uid is not None:
        print("read session uid: " + str(uid))
    team_name = data["team_name"]
    allow_join = data["allow_join"]

    # 检查用户是否在战队里
    user = User.objects.get(pk=uid)
    if user is None:
        return error_template(ExceptionEnum.USER_NOT_FOUND.value, status=404)
    custom_user = CustomUser.objects.get(user=user)
    if custom_user.team is not None:
        team = Team.objects.get(pk=custom_user.team.id)
        response_data = {"team_name": team.team_name, }
        return error_template("用户已有战队", data=response_data, status=403)

    if Team.objects.filter(team_name=team_name).exists():
        return error_template(ExceptionEnum.NAME_EXIST.value, status=409)

    new_team = Team(
        team_name=team_name,
        leader=user,
        allow_join=allow_join,
        member_count=1
    )
    new_team.save()

    custom_user.team = new_team
    custom_user.save()

    response_data = {"team_name": team_name, }
    return success_template("成功创建战队", data=response_data)


@login_required
def del_team(request):
    """
    DELETE
    @payload
    {
        "action": "del_team",
        "data": {
            "password": "123",
        }
    }
    if team_name in team.team_name.all() and leader_id == team.leader_id
        del team
    还需要把所有 team_id = team 的 CustomUser 的 team_id 改为 None
    """
    if request.method != "DELETE":
        return error_template(ExceptionEnum.INVALID_REQUEST_METHOD.value, status=405)

    if not request.user.is_authenticated:
        return error_template(ExceptionEnum.USER_NOT_LOGIN.value, status=403)

    data = request.params["data"]
    uid = request.session.get('_auth_user_id')
    password = data["password"]
    user = User.objects.get(pk=uid)
    user = authenticate(request, username=user.username, password=password)
    if user is None:
        return error_template("密码错误", status=403)
    if user.custom_user.team is None:
        return error_template(ExceptionEnum.TEAM_NOT_FOUND.value, status=404)
    team = Team.objects.get(pk=user.custom_user.team.id)
    if team is None:
        return error_template(ExceptionEnum.TEAM_NOT_FOUND.value, status=404)

    if team.leader != user:
        return error_template(ExceptionEnum.NOT_LEADER.value, status=403)

    CustomUser.objects.filter(team=team).update(team=None)
    team.delete()
    return success_template("成功删除团队", status=204)


@login_required
def join_team(request):
    """
    用户加入队伍
    POST 数据样例：
    {
        "action": "join_team",
        "data": {
            "team_name": "ezctf"
        }
    }
    """
    if request.method != "POST":
        return error_template(ExceptionEnum.INVALID_REQUEST_METHOD.value, status=405)

    if not request.user.is_authenticated:
        return error_template(ExceptionEnum.USER_NOT_LOGIN.value, status=403)

    data = request.params["data"]
    team_name = data["team_name"]
    uid = request.session.get('_auth_user_id')
    user = User.objects.get(pk=uid)
    if user is None:
        return error_template(ExceptionEnum.USER_NOT_FOUND.value, status=404)
    custom_user = CustomUser.objects.get(user=user)

    team = Team.objects.get(team_name=team_name)
    if team is None:
        return error_template(ExceptionEnum.TEAM_NOT_FOUND.value, status=404)

    if custom_user.team is not None:
        return error_template(ExceptionEnum.UNAUTHORIZED.value, status=403)

    if team.allow_join:  # 允许加入，无需审核
        custom_user.team = team
        team.member_count += 1
        custom_user.save()
        team.save()
        send_message(receiver_id=user.id, origin_id=team.leader.id, msg="欢迎加入" + str(team.team_name),
                     msg_type=Message.MessageType.CHAT.value)
        return success_template(SuccessEnum.REQUEST_SUCCESS.value)

    # 发送加入申请
    if Message.objects.filter(receiver=team.leader, origin=user,  # APPLICATION = 3
                              msg_type=Message.MessageType.APPLICATION.value).exists():
        return error_template("请求已存在", status=409)

    msg = "希望加入你的队伍"
    send_message(team.leader.id, user.id, msg=msg, msg_type=Message.MessageType.APPLICATION.value)  # APPLICATION = 3
    return success_template("申请发送成功")


@login_required
def quit_team(request):
    """
    用户退出队伍
    GET 数据样例：
    {
        "action": "quit_team",
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
    custom_user = CustomUser.objects.get(user=user)

    if custom_user.team is None:
        return error_template(ExceptionEnum.UNAUTHORIZED.value, status=403)
    team = Team.objects.get(pk=custom_user.team.id)
    if team is None:
        return error_template(ExceptionEnum.TEAM_NOT_FOUND.value, status=404)

    if team.leader == user:  # 如果用户是队长
        teammates = CustomUser.objects.filter(team=team)
        new_leader = teammates.first()
        if new_leader is None:  # 没有队员，战队自动删除
            team.delete()
            return success_template("已解散战队", status=204)
        else:  # 有队员，队长自动分配给队员
            msg = str(user.username + "将战队转交给了" + new_leader.user.username)
            for each in teammates:
                send_message(new_leader.user.id, each.user.id, msg, msg_type=Message.MessageType.CHAT.value)  # CHAT = 1
            team.leader = new_leader.user
    else:
        msg = user.username + "退出了战队"
        send_message(receiver_id=team.leader.id, origin_id=user.id, msg=msg, msg_type=Message.MessageType.CHAT.value)

    team.member_count -= 1
    custom_user.team = None
    team.save()
    custom_user.save()

    return success_template("成功退出团队")


def search_team(request):
    """
    搜索队伍
    GET  /api/common/team?action=search_team  HTTP/1.1
    {
        "action": "search_team",
        "keyword": "ez",
    }
    """
    if request.method != "GET":
        return error_template(ExceptionEnum.INVALID_REQUEST_METHOD.value, status=405)

    keyword = request.params["keyword"]
    if keyword != "":
        teams = Team.objects.filter(team_name__icontains=keyword)
    else:
        teams = Team.objects.all()

    if not teams:
        return error_template(ExceptionEnum.TEAM_NOT_FOUND.value, status=404)

    team_list = []
    for team in teams:
        leader = User.objects.get(pk=team.leader.id)
        team_info = {
            "team_name": team.team_name,
            "leader_name": leader.username,
            "leader_email": leader.email,
            "member_count": team.member_count,
            "allow_join": team.allow_join,
        }
        team_list.append(team_info)

    res_data = {
        "team_list": team_list,
        "total": len(team_list)
    }

    return success_template(SuccessEnum.QUERY_SUCCESS.value, data=res_data)


@login_required
def change_team_name(request):
    """
    队长更改战队名称
    PUT /api/common/team?action=change_team_name HTTP/1.1
    {
        "action": "change_team_name",
        "data": {
            "new_team_name": "Ezctf",
        }
    }
    """
    if request.method != "PUT":
        return error_template(ExceptionEnum.INVALID_REQUEST_METHOD.value, status=405)

    if not request.user.is_authenticated:
        return error_template(ExceptionEnum.USER_NOT_LOGIN.value, status=403)

    data = request.params["data"]
    uid = request.session.get('_auth_user_id')
    new_team_name = data["new_team_name"]
    user = User.objects.get(pk=uid)
    if user is None:
        return error_template(ExceptionEnum.USER_NOT_FOUND.value, status=404)

    if user.custom_user.team is None:
        return error_template(ExceptionEnum.NOT_LEADER.value, status=403)
    team = Team.objects.get(pk=user.custom_user.team.id)
    if team is None:
        return error_template(ExceptionEnum.TEAM_NOT_FOUND.value, status=404)

    if team.leader != user:
        return error_template(ExceptionEnum.NOT_LEADER.value, status=403)

    if Team.objects.filter(team_name=new_team_name).exists():
        return error_template(ExceptionEnum.NAME_EXIST.value, status=409)

    team.team_name = new_team_name
    team.save()
    response_data = {"team_name": new_team_name, }
    return success_template(SuccessEnum.MODIFICATION_SUCCESS.value, data=response_data)


@login_required
def change_team_leader(request):
    """
    队长更改战队名称
    PUT /api/common/team?action=change_team_name HTTP/1.1
    {
        "action": "change_team_leader",
        "data": {
            "new_leader_name": "juanboy",
        }
    }
    """
    if request.method != "PUT":
        return error_template(ExceptionEnum.INVALID_REQUEST_METHOD.value, status=405)

    if not request.user.is_authenticated:
        return error_template(ExceptionEnum.USER_NOT_LOGIN.value, status=403)

    data = request.params["data"]
    # 用户校验
    new_leader_name = data["new_leader_name"]
    uid = request.session.get('_auth_user_id')
    user = User.objects.get(pk=uid)
    new_leader = User.objects.get_by_natural_key(new_leader_name)
    if user is None or new_leader is None:  # 检测新旧队长用户是否正确读取
        return error_template(ExceptionEnum.USER_NOT_FOUND.value, status=404)
    custom_user = CustomUser.objects.get(user=user)
    custom_leader = CustomUser.objects.get(user=new_leader)

    if custom_user.team is None:  # 检测用户是否在战队内
        return error_template(ExceptionEnum.NOT_LEADER.value, status=403)
    team = Team.objects.get(pk=custom_user.team.id)
    if team.leader != user:  # 检测队长权限
        return error_template(ExceptionEnum.NOT_LEADER.value, status=403)

    if custom_leader.team != team:  # 检测新队长战队归属
        return error_template(ExceptionEnum.UNAUTHORIZED.value, data=None, status=403)
    team.leader = new_leader
    team.save()

    response_data = {
        "team_name": team.team_name,
        "new_leader_name": team.leader.username,
    }
    return success_template(SuccessEnum.MODIFICATION_SUCCESS.value, data=response_data, status=200)


@login_required
def verify_apply(request):
    """
    POST
    @payload:
    {
        "action": "verify_apply",
        "data": {
            "applicant": "juanboy",
            "accept": true / false,  # 注意布尔值不要打双引号
        },
    }
    @return:
    {
        "ret": "success" / "error",
        "msg": "审核已生效" / else
    }
    """
    if request.method != "POST":
        return error_template(ExceptionEnum.INVALID_REQUEST_METHOD.value, data=None, status=405)

    if not request.user.is_authenticated:
        return error_template(ExceptionEnum.USER_NOT_LOGIN.value, data=None, status=403)

    data = request.params["data"]
    uid = request.session.get('_auth_user_id')
    applicant = data["applicant"]
    accept_or_not = data["accept"]

    user = User.objects.get(pk=uid)
    if user is None:
        return error_template(ExceptionEnum.USER_NOT_FOUND.value, data=None, status=404)

    custom_user = CustomUser.objects.get(user=user)
    if custom_user.team is None:
        return error_template(ExceptionEnum.TEAM_NOT_FOUND.value, data=None, status=404)
    team = Team.objects.get(pk=custom_user.team.id)
    if team is None:
        return error_template(ExceptionEnum.TEAM_NOT_FOUND.value, data=None, status=404)

    if team.leader != user:
        return error_template(ExceptionEnum.NOT_LEADER.value, data=None, status=403)
    applicant = User.objects.get_by_natural_key(applicant)

    if applicant is None:
        return error_template(ExceptionEnum.USER_NOT_FOUND.value, data=None, status=404)

    applications = Message.objects.filter(receiver_id=user.id,
                                          origin_id=applicant.id,
                                          msg_type=Message.MessageType.APPLICATION.value,
                                          is_active=True)
    if not applications:
        return error_template(ExceptionEnum.MESSAGE_NOT_FOUND.value, data=None, status=404)

    if accept_or_not:
        custom_applicant = CustomUser.objects.get(user_id=applicant.id)
        custom_applicant.team = team  # 申请者入队
        team.member_count += 1  # 队伍人员数量 + 1
        custom_applicant.save()  # CHAT.value = 1
        send_message(user.id, applicant.id, "欢迎加入" + str(team.team_name), msg_type=Message.MessageType.CHAT.value)
    else:
        send_message(user.id, applicant.id, str(team.team_name) + "拒绝了你的申请",
                     msg_type=Message.MessageType.CHAT.value)

    applications.update(checked=True, is_active=False)
    return success_template("审核已生效", status=200)


@login_required
def invite(request):
    """
    POST
    {
        "action": "invite",
        "data": {
            "invitee": "juanboy",  # 受邀用户的用户名
        }
    }
    """
    if request.method != "POST":
        return error_template(ExceptionEnum.INVALID_REQUEST_METHOD.value, data=None, status=405)

    if not request.user.is_authenticated:
        return error_template(ExceptionEnum.USER_NOT_LOGIN.value, data=None, status=403)

    data = request.params["data"]
    uid = request.session.get('_auth_user_id')
    invitee_name = data["invitee"]

    user = User.objects.get(pk=uid)
    invitee = User.objects.get_by_natural_key(invitee_name)
    if user is None or user.is_active is False:
        return error_template(ExceptionEnum.UNAUTHORIZED.value, status=403)
    if invitee is None or invitee.is_active is False:
        res_data = {"username": invitee_name, }
        return error_template(ExceptionEnum.USER_NOT_FOUND.value, data=res_data, status=404)

    custom_user = CustomUser.objects.get(user=user)
    if custom_user.team is None:
        return error_template(ExceptionEnum.TEAM_NOT_FOUND.value, data=None, status=404)
    team = Team.objects.get(pk=custom_user.team.id)
    if team is None:
        return error_template(ExceptionEnum.TEAM_NOT_FOUND.value, status=404)

    if team.leader != user:
        return error_template(ExceptionEnum.NOT_LEADER.value, status=403)

    msg = str(team.team_name)
    send_message(invitee.id, user.id, msg=msg, msg_type=Message.MessageType.INVITATION.value)  # INVITATION.value = 4
    return success_template(SuccessEnum.POST_SUCCESS.value)


@login_required
def kick_out(request):
    """
    POST
    {
        "action": "kick_out",
        "data": {
            "username": "momoyeyu",
        }
    }
    """
    data = request.params["data"]
    username = data["username"]
    uid = request.session.get("_auth_user_id")
    if uid is None:
        return error_template(ExceptionEnum.USER_NOT_LOGIN.value, status=403)
    user = User.objects.get(pk=uid)
    if user is None:
        return error_template(ExceptionEnum.USER_NOT_LOGIN.value, status=403)
    if user.custom_user.team is None or user.custom_user.team.leader != user:
        return error_template(ExceptionEnum.NOT_LEADER.value, status=403)
    team = Team.objects.get(pk=user.custom_user.team_id)
    if user.username == username:
        return error_template(ExceptionEnum.UNAUTHORIZED.value, status=403)
    kick = User.objects.get_by_natural_key(username)
    if kick is None or kick.is_active is False:
        return error_template(ExceptionEnum.USER_NOT_FOUND.value, status=404)
    c_kick = CustomUser.objects.get(user=kick)
    if c_kick.team != team:
        return error_template(ExceptionEnum.UNAUTHORIZED.value, status=403)
    c_kick.team = None
    team.member_count -= 1
    c_kick.save()
    team.save()
    send_message(receiver_id=kick.id, origin_id=user.id, msg=team.team_name, msg_type=Message.MessageType.KICKOUT.value)
    return success_template(SuccessEnum.REQUEST_SUCCESS.value)


@login_required
def accept(request):
    """
    POST
    {
        "action": "accept",
        "data": {
            "inviter": "juanboy",
            "team_name": "ezctf",
            "accept": true,
        }
    }
    """
    if request.method != "POST":
        return error_template(ExceptionEnum.INVALID_REQUEST_METHOD.value, data=None, status=405)

    if not request.user.is_authenticated:
        return error_template(ExceptionEnum.USER_NOT_LOGIN.value, data=None, status=403)

    data = request.params["data"]
    uid = request.session.get('_auth_user_id')
    if uid is None:
        return error_template(ExceptionEnum.USER_NOT_LOGIN.value, status=403)
    inviter_name = data["inviter"]
    team_name = data["team_name"]
    accept_or_not = data["accept"]
    # check users
    user = User.objects.get(pk=uid)
    inviter = User.objects.get_by_natural_key(inviter_name)
    if inviter is None or inviter.is_active is False:
        res_data = {"username": inviter_name, }
        return error_template(ExceptionEnum.USER_NOT_FOUND.value, data=res_data, status=404)
    # check messages
    invitations = Message.objects.filter(receiver=user,
                                         origin=inviter,
                                         msg_type=Message.MessageType.INVITATION.value,  # INVITATION.value = 4
                                         is_active=True)
    if not invitations:
        return error_template(ExceptionEnum.MESSAGE_NOT_FOUND.value, status=404)

    # 邀请信息已经处理，删除所有邀请
    invitations.update(checked=True, is_active=False)

    custom_user = CustomUser.objects.get(user=user)
    custom_origin = CustomUser.objects.get(user=inviter)
    team = Team.objects.get(team_name=team_name)
    if team is None:
        return error_template(ExceptionEnum.TEAM_NOT_FOUND.value, status=404)

    if accept_or_not:
        team.member_count += 1
        custom_user.team = team
        team.save()
        custom_user.save()
        msg = "接受邀请"
        res_data = {"team_name": team.team_name, }
        send_message(inviter.id, user.id, msg=msg, msg_type=Message.MessageType.CHAT.value)  # CHAT.value = 1
        return success_template(SuccessEnum.REQUEST_SUCCESS.value, data=res_data)
    else:
        msg = "拒绝邀请"
        send_message(inviter.id, user.id, msg=msg, msg_type=Message.MessageType.CHAT.value)  # CHAT.value = 1
        return success_template(SuccessEnum.REQUEST_SUCCESS.value)
