from django.http import HttpResponse
from django.http import JsonResponse
from utils import get_request_params
from common.models import Team
from django.contrib.auth.models import User


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

    else:
        return JsonResponse({'ret': 1, 'msg': 'Unsupported request!'})


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
    leader = User.objects.get(pk=info['leader_id'])
    if leader.team_id is not None:
        return JsonResponse({
            'return': 1,
            "message": "用户已有战队！"
        })

    #
    record = Team.objects.create(
        team_name=info['team_name'],
        leader_id=info['leader_id'],
        allow_join=info['allow_join'],
        member_count=1
    )

    return JsonResponse({
        'ret': 0,
        'id': record.id
    })


def del_team(request):
    """
    队长删除战队
    DELETE 获取数据样例：
    {
        "action":"del_team",
        "data":{
            "leader_id":"1",
            "team_name":"ezctf",
        }
    }
    if team_name in team.team_name.all() and leader_id == team.leader_id
        del team
    """
    info = request.params['data']
    leader_id = info['leader_id']
    team_name = info['team_name']
    # 查询团队是否存在
    try:
        team = Team.objects.get(team_name=team_name)
    except Team.DoesNotExist:
        # 团队不存在，返回错误响应
        return JsonResponse({
            'return': 1,
            "message": "团队" + team_name + "不存在!"
        }, status=404)

    # 验证 leader_id 是否匹配
    if team.leader_id.id != leader_id:
        # leader_id 不匹配，无法删除团队，返回错误响应
        return JsonResponse({
            'return': 1,
            "message": "无法删除团队，权限不足!"
        }, status=403)

    # 删除团队
    team.delete()

    # 返回成功响应
    return JsonResponse({
        'return': 0,
        "message": "成功删除团队"}, status=204)

    return HttpResponse()


def join_team(request):
    """ 用户加入队伍 """
    # TODO

    return HttpResponse()


def quit_team(request):

    return HttpResponse()


def is_user_in_team(user_id, team_id):
    """
    if user in team
        return true
    else
        return false
    """
    try:
        user = User.objects.get(pk=user_id)
        if user.team_id == team_id:  # 检查用户的team_id是否与给定的团队ID相匹配
            return True
        else:
            return False
    except User.DoesNotExist:
        return False

