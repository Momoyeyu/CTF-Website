from django.http import HttpResponse
from django.http import JsonResponse
from utils import get_request_params
from django.contrib.auth.models import User
from common.models import CustomUser
from django.contrib.auth import authenticate, login
import json

"""
此文件仅处理 user表 数据
"""


def dispatcher(request):
    # 将请求参数统一放入request 的 params 属性中，方便后续处理

    request.params = get_request_params(request)
    """# GET请求 参数在url中，同过request 对象的 GET属性获取
    if request.method == 'GET':
        request.params = request.GET

    # POST/PUT/DELETE 请求 参数 从 request 对象的 body 属性中获取
    elif request.method in ['POST', 'PUT', 'DELETE']:
        # 根据接口，POST/PUT/DELETE 请求的消息体都是 json格式
        request.params = json.loads(request.body)"""

    # 根据不同的action分派给不同的函数进行处理
    action = request.params['action']
    if action == 'login':
        return user_login(request)
    elif action == 'register':
        return user_register(request)
    elif action == 'modify_user':
        return modify_user(request)
    elif action == 'del_user':
        return del_user(request)

    else:
        return JsonResponse({'ret': 1, 'msg': 'Unsupported request!'})


def user_login(request):
    """
    用户登录，返回用户数据
    @payload:
    {
        "action":"login",
        "data":{
            "username_or_email":"momoyeyu",
            "password":"123",
        }
    }
    @return:
    {
        'ret'
        'msg'
        'data': {
            "user_id"
            "username"
        }
    }
    """
    if request.method != 'POST':
        return JsonResponse({
            'ret': 'error',
            'msg': 'Unsupported request method.',
        })

    try:
        info = request.params['data']
        username_or_email = info['username_or_email']
        password = info['password']

        user = None
        if '@' in username_or_email:
            # 如果输入包含 '@'，则尝试使用电子邮件进行身份验证
            user = authenticate(request, email=username_or_email, password=password)
        else:
            # 否则，尝试使用用户名进行身份验证
            user = authenticate(request, username=username_or_email, password=password)

        if user is not None:
            login(request, user)
            # 用户已成功登录
            return JsonResponse({
                'ret': 'success',
                'msg': '登录成功',
                'data': {
                    'user_id': user.id,
                    'username': user.username,
                }
            })
        else:
            # 登录失败
            return JsonResponse({
                'ret': 'error',
                'msg': '！登陆失败，请检查你的信息',
            })

    except json.JSONDecodeError:
        # 请求数据无法解析
        return JsonResponse({
            'ret': 'error',
            'msg': 'Invalid JSON data in the request.',
        })


def user_register(request):
    """
    用户注册，创建新的User，CustomUser，并将CustomUser的user_id设置为User的id
    @payload:
    {
        "action":"register",
        "data":{
            "username": "momoyeyu",
            "password": "123",
            "email": "momoyeyu@outlookcom",
            "valid": "123456"
        }
    }
    """
    if request.method != 'POST':
        return JsonResponse({
            'ret': 'error',
            'msg': 'Invalid request method.',
            'data': None
        })

    info = request.params['data']
    username = info['username']
    password = info['password']
    email = info['email']

    # 验证用户输入
    if not username or not password or not email:
        return JsonResponse({
            'ret': 'error',
            'msg': '请输入完整信息',
            'data': None
        }, status=400)

    if User.objects.filter(username=username).exists():
        return JsonResponse({
            'ret': 'error',
            'msg': '用户名已被使用',
            'data': None
        })

    if User.objects.filter(email=email).exists():
        return JsonResponse({
            'ret': 'error',
            'msg': '邮箱已被使用',
            'data': None
        })

    # TODO 验证码

    # 创建 User，create_user() 会自动处理密码的加密
    user = User.objects.create_user(username=username, password=password, email=email)

    # 创建 CustomUser，关联到 User
    custom_user = CustomUser(user_id=user.id, score=0)
    custom_user.save()

    return JsonResponse({
        'ret': 'success',
        'msg': '注册成功',
        'data': {
            'username': user.username,
            'user_id': user.id
        }
    })


def modify_user(request):
    """
    处理用户更新信息
    """
    # TODO

    return HttpResponse()


def del_user(request):
    """ 用户注销账号，删除数据库中与该用户有关的所有数据 """
    # TODO

    return HttpResponse()



