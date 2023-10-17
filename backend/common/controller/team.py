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
    action = request.params['action']
    if action == 'create_team':
        return create_team(request)
    elif action == 'del_team':
        return del_team(request)
    elif action == 'join_team':
        return join_team(request)
    elif action == 'quit_team':
        return quit_team(request)
    elif action == 'search_team':
        return search_team(request)

    else:
        return JsonResponse({'return': 'error', 'message': 'Unsupported request!'})


def create_team(request):
    """
    队长创建战队
    POST 获取数据样例：
    {
        "action":"create_team",
        "data":{
            "leader_id":"1",
            "team_name":"ezctf",
            "allow_join":"true"
        }
    }
    注意 allow_join 的格式，我不知道 json 可不可以自动解析
    """
    info = request.params['data']

    # 检查用户是否在战队里
    leader = None
    try:
        leader = CustomUser.objects.get(user_id=info['leader_id'])
    except CustomUser.DoesNotExist:
        return JsonResponse({
            'ret': 'error',
            "msg": "队长用户不存在"
        })

    if leader.team_id is not None:
        return JsonResponse({
            'ret': 'error',
            "msg": "用户已有战队"
        })

    if Team.objects.filter(team_name=info['team_name']).exists():
        return JsonResponse({
            'ret': 'error',
            'msg': '战队名已被使用',
        })

    new_team = Team.objects.create(
        team_name=info['team_name'],
        leader_id=info['leader_id'],
        allow_join=info['allow_join'],
        member_count=1
    )
    leader.team_id = new_team.id

    return JsonResponse({
        'ret': 'success',
        'msg': '成功创建战队'
    })


def del_team(request):
    """
    队长删除战队
    DELETE 获取数据样例：
    {
        "action":"del_team",
        "data":{
            "leader_id":"1",
            "password":"123"
        }
    }
    if team_name in team.team_name.all() and leader_id == team.leader_id
        del team
    还需要把所有 team_id = team 的 CustomUser 的team_id 改为 None
    """
    if request.method != "DELETE":
        return JsonResponse({
            "ret": "error",
            "msg": "Invalid request method"
        }, status=405)

    info = request.params['data']
    leader_id = info['leader_id']
    leader_password = info['password']

    leader = None
    try:
        leader = User.objects.get(pk=info['leader_id'], password=info['leader_password'])
    except User.DoesNotExist:
        return JsonResponse({
            'ret': 'error',
            "msg": "密码错误"
        })

    # 查询团队是否存在
    team = None
    try:
        team = Team.objects.get(pk=leader.custom_user.team_id)
    except Team.DoesNotExist:
        # 团队不存在，返回错误响应
        return JsonResponse({
            'ret': 'error',
            "msg": "战队不存在"
        }, status=404)

    # 验证 leader_id 是否匹配
    if team.leader_id.id != leader_id:
        # leader_id 不匹配，无法删除团队，返回错误响应
        return JsonResponse({
            'ret': 'error',
            "msg": "无法删除团队，权限不足"
        }, status=403)

    # 删除团队
    team.delete()

    # 返回成功响应
    return JsonResponse({
        'ret': 'success',
        "msg": "成功删除团队"
    }, status=204)


def join_team(request):
    """
    用户加入队伍
    PUT 数据样例：
    {
        "action":"join_team",
        "data":{
            "user_id":"1",
            "team_name":"ezctf",
        }
    }
    """
    if request.method != "PUT":
        return JsonResponse({
            "ret": "error",
            "msg": "Invalid request method"
        }, status=405)

    info = request.params['data']
    user_id = info['user_id']
    team_name = info['team_name']

    user = None
    try:
        user = CustomUser.objects.get(user_id=info['user_id'])
    except CustomUser.DoesNotExist:
        return JsonResponse({
            'ret': 'error',
            "msg": "用户不存在"
        }, status=404)

    # 查询团队是否存在
    team = None
    try:
        team = Team.objects.get(team_name=team_name)
    except Team.DoesNotExist:
        # 团队不存在，返回错误响应
        return JsonResponse({
            'ret': 'error',
            "msg": "战队\"" + team_name + "\"不存在"
        }, status=404)

    if not team.allow_join:
        return JsonResponse({
            'ret': 'error',
            "msg": "战队\"" + team_name + "\"不允许加入，需要队长邀请"
        }, status=404)

    team.member_count += 1
    user.team_id = team.id

    team.save()
    user.save()

    # 返回成功响应
    return JsonResponse({
        'ret': 'success',
        "msg": "成功加入团队"
    }, status=200)


def quit_team(request):
    """
    用户加入队伍
    PUT 数据样例：
    {
        "action":"quit_team",
        "data":{
            "user_id":"1",
        }
    }
    """
    if request.method != "PUT":
        return JsonResponse({
            "ret": "error",
            "msg": "Invalid request method"
        }, status=405)

    info = request.params['data']
    user_id = info['user_id']

    user = None
    try:
        user = CustomUser.objects.get(user_id=info['user_id'])
    except CustomUser.DoesNotExist:
        return JsonResponse({
            'ret': 'error',
            "msg": "用户不存在"
        }, status=404)

    team = Team.objects.get(pk=user.team_id)

    if team.leader_id == user_id:
        return JsonResponse({
            'ret': 'error',
            "msg": "队长无法退出战队，只能解散战队"
        }, status=403)

    team.member_count -= 1
    user.team_id = None

    team.save()
    user.save()

    # 返回成功响应
    return JsonResponse({
        'ret': 'success',
        "msg": "成功退出团队"
    }, status=200)


def is_user_in_team(user_id, team_id):
    """
    if user in team
        return true
    else
        return false
    """
    try:
        user = CustomUser.objects.get(user_id=user_id)
        if user.team_id == team_id:  # 检查用户的team_id是否与给定的团队ID相匹配
            return True
        else:
            return False
    except User.DoesNotExist:
        return False


def search_team(request):
    """
    用户加入队伍
    GET  /api/common/team?action=search_team  HTTP/1.1
    {
        "action":"search_team",
        "keyword": "xxx",
    }
    """
    keyword = request.params['keyword']

    if keyword:
        # 直接查询 team_name 包含关键字且 allow_join 为 True 的队伍
        teams = Team.objects.filter(team_name__icontains=keyword, allow_join=True)
    else:
        teams = Team.objects.filter(allow_join=True)

    if not teams:
        return JsonResponse({
            'ret': 'error',
            'msg': '没有找到匹配的队伍',
        }, status=404)

    return
