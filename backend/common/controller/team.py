from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.http import JsonResponse
from utils import get_request_params
from common.models import Team
from django.contrib.auth.models import User
from common.models import CustomUser


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
            "leader_name": "momoyeyu",
            "team_name": "ezctf",
            "allow_join": "true"
        }
    }
    """
    if request.method != "POST":
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

    # 检查用户是否在战队里
    user = None
    try:
        user = User.objects.get_by_natural_key(data["leader_name"])
        custom_user = CustomUser.objects.get(user=user)
        if custom_user.team_id is not None:
            team = Team.objects.get(pk=custom_user.team_id)
            return JsonResponse({
                "ret": "error",
                "msg": "用户已有战队",
                "data": {
                    "team_name": team.team_name
                }
            }, status=400)

        if Team.objects.filter(team_name=data["team_name"]).exists():
            return JsonResponse({
                "ret": "error",
                "msg": "战队名已被使用",
            }, status=400)

        new_team = Team(
            team_name=data["team_name"],
            leader_name=data["leader_name"],
            allow_join=data["allow_join"],
            member_count=1
        )
        custom_user.team_id = new_team.id

        custom_user.save()
        new_team.save()

        return JsonResponse({
            "ret": "success",
            "msg": "成功创建战队",
            "data": {
                "team_name": data["team_name"]
            }
        }, status=200)

    except User.DoesNotExist:
        return JsonResponse({
            "ret": "error",
            "msg": "用户不合法！"
        }, status=404)


def del_team(request):
    """
    队长删除战队
    DELETE 获取数据样例：
    {
        "action": "del_team",
        "data": {
            "username": "momoyeyu",
            "password": "123",
            "team_name": "ezctf"
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
    team_name = data["team_name"]

    try:
        user = authenticate(request, email=username, password=password)
        try:
            team = Team.objects.get(pk=user.custom_user.team_id)
            if team.leader_id != user.id:
                # leader_id 不匹配，无法删除团队，返回错误响应
                return JsonResponse({
                    "ret": "error",
                    "msg": "无法删除团队，权限不足"
                }, status=403)

            if team.team_name == team_name:
                CustomUser.objects.filter(team_id=team.id).update(team_id=None)
                team.delete()
                return JsonResponse({
                    "ret": "success",
                    "msg": "成功删除团队"
                }, status=204)
            else:
                return JsonResponse({
                    "ret": "error",
                    "msg": "战队名称不匹配"
                }, status=400)

        except Team.DoesNotExist:
            # 团队不存在，返回错误响应
            return JsonResponse({
                "ret": "error",
                "msg": "战队不存在"
            }, status=404)

    except User.DoesNotExist:
        return JsonResponse({
            "ret": "error",
            "msg": "密码错误"
        })


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
    team_name = data["team_name"]

    user = None
    try:
        user = User.objects.get_by_natural_key(username)
        custom_user = CustomUser.objects.get(user=user)

        try:
            team = Team.objects.get(team_name=team_name)

            if custom_user.team_id is not None:
                if team.id == custom_user.team_id:
                    return JsonResponse({
                        "ret": "error",
                        "msg": "您已在此战队，不要重复加入"
                    }, status=400)
                else:
                    return JsonResponse({
                        "ret": "error",
                        "msg": "您已在其他战队"
                    }, status=400)

            if not team.allow_join:
                msg = "战队 " + team_name + " 需要队长邀请才能加入"
                leader = User.objects.get(pk=team.leader_id)
                return JsonResponse({
                    "ret": "error",
                    "msg": msg,
                    "data": {
                        "leader_email": leader.email
                    }
                }, status=400)

            # 正常加入
            team.member_count += 1
            custom_user.team_id = team.id

            team.save()
            custom_user.save()

            # 返回成功响应
            return JsonResponse({
                "ret": "success",
                "msg": "成功加入团队",
                "data": {
                    "team_name": team_name
                }
            }, status=200)

        except Team.DoesNotExist:
            # 团队不存在，返回错误响应
            msg = "战队 " + str(team_name) + " 不存在"
            return JsonResponse({
                "ret": "error",
                "msg": msg
            }, status=404)

    except User.DoesNotExist:
        return JsonResponse({
            "ret": "error",
            "msg": "非法用户操作"
        }, status=404)


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
    team_name = data["team_name"]

    try:
        user = User.objects.get_by_natural_key(username)
        custom_user = CustomUser.objects.get(user=user)
        try:
            team = Team.objects.get(team_name=team_name)

            if team.leader_id == user.id:
                return JsonResponse({
                    "ret": "error",
                    "msg": "队长无法退出战队，请在和队员协商后转让队长或解散战队"
                }, status=403)

            team.member_count += 1
            custom_user.team_id = None

            team.save()
            custom_user.save()

            return JsonResponse({
                "ret": "success",
                "msg": "成功退出团队"
            }, status=200)

        except Team.DoesNotExist:
            return JsonResponse({
                "ret": "error",
                "msg": "战队不存在"
            }, status=404)

    except ObjectDoesNotExist:
        return JsonResponse({
            "ret": "error",
            "msg": "用户不存在"
        }, status=404)


def search_team(request):
    """
    搜索队伍
    GET  /api/common/team?action=search_team  HTTP/1.1
    {
        "action": "search_team",
        "data": {
            "keyword": "ez"
        }
    }
    """
    if request.method != "GET":
        return JsonResponse({
            "ret": "error",
            "msg": "Invalid request method"
        }, status=405)

    data= request.params["data"]
    keyword = data["keyword"]

    if keyword:
        # 直接查询 team_name 包含关键字且 allow_join 为 True 的队伍
        teams = Team.objects.filter(team_name__icontains=keyword)
    else:
        teams = Team.objects.values()

    if not teams:
        # 如果没有找到匹配的队伍
        return JsonResponse({
            "ret": "error",
            "msg": "没有找到匹配的队伍",
        }, status=404)

    team_list = []
    for team in teams:
        team_info = {
            "team_name": team.team_name,
            "leader_name": team.leader.username,
            "leader_email": team.leader.email,
            "member_count": team.member_count,
            "allow_join": team.allow_join,
        }
        team_list.append(team_info)

    return JsonResponse({
        "ret": "success",
        "msg": "匹配的队伍信息",
        "data": team_list
    }, status=200)


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
    old = data["old_team_name"]
    new = data["new_team_name"]
    try:
        team = Team.objects.get(team_name=old)
        if team.leader.username == username:
            if Team.objects.filter(team_name=new):
                return JsonResponse({
                    "ret": "error",
                    "msg": "队名已被使用",
                }, status=409)

            team.team_name = new
            team.save()
            return JsonResponse({
                "ret": "success",
                "msg": "成功修改队伍名称",
                "data": {
                    "team_name": new
                }
            }, status=200)
        else:
            return JsonResponse({
                "ret": "error",
                "msg": "权限不足",
            }, status=403)

    except ObjectDoesNotExist:
        return JsonResponse({
            "ret": "error",
            "msg": "队伍不存在"
        }, status=404)

