from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.http import HttpResponse
from django.http import JsonResponse
from utils import get_request_params
from common.models import Team, Message, CustomUser
from django.contrib.auth.models import User
from utils import ExceptionEnum, error_template, success_template, send_message


def dispatcher(request):
    # 将请求参数统一放入request 的 params 属性中，方便后续处理

    # 经过此函数处理，request.params 里的对象已经转为 python 字典，数据类型也已经经过处理
    request.params = get_request_params(request)

    # 根据不同的action分派给不同的函数进行处理
    action = request.params["action"]
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

    else:
        return JsonResponse({
            "ret": "error",
            "msg": "Unsupported request!"
        }, status=404)


def create_team(request):
    """
    队长创建战队
    POST 获取数据样例：
    {
        "action": "create_team",
        "data":{
            "username": "momoyeyu",
            "team_name": "ezctf",
            "allow_join": "true"
        }
    }
    """
    if request.method != "POST":
        return error_template(ExceptionEnum.INVALID_REQUEST_METHOD, status=405)

    if not request.user.is_authenticated:
        return error_template(ExceptionEnum.USER_NOT_LOGIN, status=403)
    data = request.params["data"]
    username = data["username"]
    team_name = data["team_name"]
    allow_join = data["allow_join"]

    # 检查用户是否在战队里
    user = User.objects.get_by_natural_key(username)
    if user is None:
        return error_template(ExceptionEnum.USER_NOT_FOUND, status=404)
    custom_user = CustomUser.objects.get(user=user)
    if custom_user.team_id is not None:
        team = Team.objects.get(pk=custom_user.team_id)
        response_data = {"team_name": team.team_name, }
        return error_template("用户已有战队", data=response_data, status=403)

    if Team.objects.filter(team_name=team_name).exists():
        return error_template(ExceptionEnum.NAME_EXIST, status=409)

    new_team = Team(
        team_name=team_name,
        leader_name=username,
        allow_join=allow_join,
        member_count=1
    )
    custom_user.team_id = new_team.id

    custom_user.save()
    new_team.save()
    response_data = {"team_name": data["team_name"], }
    return success_template("成功创建战队", data=response_data)


def del_team(request):
    """
    队长删除战队
    DELETE 获取数据样例：
    {
        "action": "del_team",
        "data": {
            "username": "momoyeyu",
            "password": "123",
        }
    }
    if team_name in team.team_name.all() and leader_id == team.leader_id
        del team
    还需要把所有 team_id = team 的 CustomUser 的 team_id 改为 None
    """
    if request.method != "DELETE":
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
    password = data["password"]

    user = authenticate(request, username=username, password=password)
    if user is None:
        return JsonResponse({
            "ret": "error",
            "msg": "密码错误"
        }, status=403)

    team = Team.objects.get(pk=user.custom_user.team_id)
    if team is None:
        return error_template(ExceptionEnum.TEAM_NOT_FOUND, status=404)

    if team.leader_id != user.id:
        return error_template(ExceptionEnum.NOT_LEADER, status=403)

    CustomUser.objects.filter(team_id=team.id).update(team_id=None)
    try:
        team.delete()
        return success_template("成功删除团队", status=204)
    except:
        return error_template("删除团队失败")


def join_team(request):
    """
    用户加入队伍
    PUT 数据样例：
    {
        "action": "join_team",
        "data": {
            "username": "momoyeyu",
            "team_name": "ezctf"
        }
    }
    """
    if request.method != "PUT":
        return error_template(ExceptionEnum.INVALID_REQUEST_METHOD, status=405)

    if not request.user.is_authenticated:
        return error_template(ExceptionEnum.USER_NOT_LOGIN, status=403)

    data = request.params["data"]
    username = data["username"]
    team_name = data["team_name"]

    user = User.objects.get_by_natural_key(username)
    if user is None:
        return error_template(ExceptionEnum.USER_NOT_FOUND, status=404)

    custom_user = CustomUser.objects.get(user=user)

    team = Team.objects.get(team_name=team_name)
    if team is None:
        return error_template(ExceptionEnum.TEAM_NOT_FOUND, status=404)

    if custom_user.team_id is not None:
        return error_template(ExceptionEnum.UNAUTHORIZED, status=403)

    leader = User.objects.get(pk=team.leader_id)
    if not team.allow_join:
        response_data = {"leader_email": leader.email, }
        msg = "战队 " + team_name + " 需要队长邀请才能加入"
        return error_template(msg, data=response_data, status=403)

    # 发送加入申请
    msg = str(username) + "希望加入你的队伍"
    message = Message(origin=user.id, receiver=leader.id, message=msg)
    message.check = False
    try:
        message.save()
        return success_template("申请发送成功")
    except IntegrityError:
        return error_template("申请发送失败")


def quit_team(request):
    """
    用户退出队伍
    PUT 数据样例：
    {
        "action": "quit_team",
        "data": {
            "username": "momoyeyu",
            "team_name": "ezctf"
        }
    }
    """
    if request.method != "PUT":
        return error_template(ExceptionEnum.INVALID_REQUEST_METHOD, status=405)

    if not request.user.is_authenticated:
        return error_template(ExceptionEnum.USER_NOT_LOGIN, status=403)

    data = request.params["data"]
    username = data["username"]
    team_name = data["team_name"]

    user = User.objects.get_by_natural_key(username)
    if user is None:
        return error_template(ExceptionEnum.USER_NOT_FOUND, status=404)

    custom_user = CustomUser.objects.get(user=user)
    team = Team.objects.get(team_name=team_name)
    if team is None:
        return error_template(ExceptionEnum.TEAM_NOT_FOUND, status=404)

    if team.leader_id == user.id:  # 如果用户是队长
        new_leader = CustomUser.objects.filter(team_id=team.id)[0]
        if new_leader is None:  # 没有队员，战队自动删除
            team.delete()
            return success_template("已解散战队", status=204)
        else:  # 有队员，队长自动分配给队员
            msg = str(user.username + "战队转交给了" + new_leader.user.username)
            send_message(new_leader.user.id, user.id, msg, msg_type="chat")
            team.leader_id = new_leader.user.id

    team.member_count -= 1
    custom_user.team_id = None

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
        return error_template(ExceptionEnum.INVALID_REQUEST_METHOD, status=405)

    keyword = request.params["keyword"]

    if keyword:
        teams = Team.objects.filter(team_name__icontains=keyword)
    else:
        teams = Team.objects.values()

    if not teams:
        return error_template(ExceptionEnum.TEAM_NOT_FOUND, status=404)

    team_list = []
    for team in teams:
        leader = User.objects.get(pk=team.leader_id)
        team_info = {
            "team_name": team.team_name,
            "leader_name": leader.username,
            "leader_email": leader.email,
            "member_count": team.member_count,
            "allow_join": team.allow_join,
        }
        team_list.append(team_info)

    return success_template("匹配的队伍信息", data=team_list)


def change_team_name(request):
    """
    队长更改战队名称
    PUT /api/common/team?action=change_team_name HTTP/1.1
    {
        "action": "change_team_name",
        "data": {
            "username": "momoyeyu",
            "old_team_name": "ezctf",
            "new_team_name": "Ezctf",
        }
    }
    """
    if request.method != "PUT":
        return error_template(ExceptionEnum.INVALID_REQUEST_METHOD, status=405)

    if not request.user.is_authenticated:
        return error_template(ExceptionEnum.USER_NOT_LOGIN, status=403)

    data = request.params["data"]
    username = data["username"]
    old_team_name = data["old_team_name"]
    new_team_name = data["new_team_name"]
    team = Team.objects.get(team_name=old_team_name)
    if team is None:
        return error_template(ExceptionEnum.TEAM_NOT_FOUND, status=404)

    if team.leader.username != username:
        return error_template(ExceptionEnum.NOT_LEADER, status=403)

    if Team.objects.filter(team_name=new_team_name):
        return error_template(ExceptionEnum.NAME_EXIST, status=409)

    team.team_name = new_team_name
    team.save()
    response_data = {"team_name": new_team_name, }
    return success_template("成功修改队伍名称", data=response_data)


def change_team_leader(request):
    """
    队长更改战队名称
    PUT /api/common/team?action=change_team_name HTTP/1.1
    {
        "action": "change_team_leader",
        "data": {
            "username": "momoyeyu",
            "new_leader_name": "juanboy",
        }
    }
    """
    if request.method != "PUT":
        return error_template(ExceptionEnum.INVALID_REQUEST_METHOD, status=405)

    if not request.user.is_authenticated:
        return error_template(ExceptionEnum.USER_NOT_LOGIN, status=403)

    data = request.params["data"]
    username = data["username"]
    new_leader_name = data["new_leader_name"]
    user = User.objects.get_by_natural_key(username)
    new_leader = User.objects.get_by_natural_key(new_leader_name)

    if user is None or new_leader is None:  # 检测新旧队长用户是否正确读取
        return error_template(ExceptionEnum.USER_NOT_FOUND, status=404)
    custom_user = CustomUser.objects.get(user_id=user.id)
    custom_leader = CustomUser.objects.get(user_id=new_leader.id)

    if custom_user.team_id is None:  # 检测用户是否在战队内
        return error_template(ExceptionEnum.NOT_LEADER, status=403)
    team = Team.objects.get(pk=custom_user.team_id)
    if team.leader_id != user.id:  # 检测队长权限
        return error_template(ExceptionEnum.NOT_LEADER, status=403)

    if custom_leader.team_id != team.id:  # 检测新队长战队归属
        return error_template(ExceptionEnum.UNAUTHORIZED, data=None, status=403)
    team.leader_id = new_leader.id
    team.save()

    response_data = {"new_leader_name": team.leader.username, }
    return success_template("成功更换队长", data=response_data, status=200)


def verify_apply(request):
    """
    POST
    @payload:
    {
        "action": "verify_apply",
        "data": {
            "username": "momoyeyu",
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
        return error_template(ExceptionEnum.INVALID_REQUEST_METHOD, data=None, status=405)

    if not request.user.is_authenticated:
        return error_template(ExceptionEnum.USER_NOT_LOGIN, data=None, status=403)

    data = request.params["data"]
    username = data["username"]
    applicant = data["applicant"]
    accept = data["accept"]

    user = User.objects.get_by_natural_key(username)

    if user is None:
        return error_template(ExceptionEnum.USER_NOT_FOUND.value, data=None, status=404)

    custom_user = CustomUser.objects.get(user_id=user.id)
    team = Team.objects.get(pk=custom_user.team_id)

    if team is None:
        return error_template(ExceptionEnum.TEAM_NOT_FOUND.value, data=None, status=404)

    if team.leader_id != user.id:
        return error_template(ExceptionEnum.NOT_LEADER.value, data=None, status=403)
    applicant = User.objects.get_by_natural_key(applicant)

    if applicant is None:
        return error_template(ExceptionEnum.USER_NOT_FOUND.value, data=None, status=404)

    applications = Message.objects.filter(receiver_id=user.id, origin_id=applicant.id, msg_type="join_team")
    if applications is None:
        return error_template(ExceptionEnum.MESSAGE_NOT_FOUND.value, data=None, status=404)

    if accept:
        custom_applicant = CustomUser.objects.get(user_id=applicant.id)
        custom_applicant.team_id = team.id  # 申请者入队
        team.member_count += 1  # 队伍人员数量 + 1
        custom_applicant.save()
        send_message(user.id, applicant.id, "欢迎加入" + str(team.team_name), msg_type="chat")
    else:
        send_message(user.id, applicant.id, str(team.team_name) + "拒绝了你的申请", msg_type="chat")

    for each in applications:
        each.delete()

    return success_template("审核已生效", data=None, status=200)
