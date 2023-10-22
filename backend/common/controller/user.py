import uuid

from django.core.mail import send_mail
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse

from backend import settings
from utils import get_request_params, is_valid_username
from django.contrib.auth.models import User
from common.models import CustomUser, Team
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
import json

"""
此文件仅处理 user表 数据
"""


def dispatcher(request):
    # 将请求参数统一放入request 的 params 属性中，方便后续处理

    request.params = get_request_params(request)
    """# GET请求 参数在url中，同过request 对象的 GET属性获取
    if request.method == "GET":
        request.params = request.GET

    # POST/PUT/DELETE 请求 参数 从 request 对象的 body 属性中获取
    elif request.method in ["POST", "PUT", "DELETE"]:
        # 根据接口，POST/PUT/DELETE 请求的消息体都是 json格式
        request.params = json.loads(request.body)"""

    # 根据不同的action分派给不同的函数进行处理
    action = request.params["action"]
    if action == "login":
        return user_login(request)
    elif action == "logout":
        return user_logout(request)
    elif action == "register":
        return user_register(request)
    elif action == "modify_user_info":
        return modify_user_info(request)
    elif action == "del_account":
        return del_account(request)

    else:
        return JsonResponse({"ret": "error", "msg": "Unsupported request!"})


def user_login(request):
    """
    用户登录，返回用户数据
    POST
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
        "ret": "success" / "error",
        "msg": "注册成功" / "报错信息"
        "data": {
            "username": "momoyeyu",
            "score": "100",
            "team_name": "ezctf",
            "is_leader": "true"
        }
    }
    """
    if request.method != "POST":
        return JsonResponse({
            "ret": "error",
            "msg": "Unsupported request method.",
        }, status=405)

    try:
        info = request.params["data"]
        username_or_email = info["username_or_email"]
        password = info["password"]

        if "@" in username_or_email:
            user = authenticate(request, email=username_or_email, password=password)
        else:
            user = authenticate(request, username=username_or_email, password=password)

        if user is not None:

            if user.is_active is False:
                return JsonResponse({
                    "ret": "error",
                    "msg": "用户未激活",
                }, status=404)
            login(request, user)
            request.session["username"] = user.username
            custom_user = CustomUser.objects.get(user_id=user.id)

            response = {"ret": "success", "msg": "登录成功", "data": {
                        "username": user.username,
                        "score": custom_user.score,
                        "team_name": None,
                        "is_leader": None
                    }
                }

            if custom_user.team_id is not None:
                team = Team.objects.get(pk=custom_user.team_id)
                response["data"]["team_name"] = team.team_name
                if team.leader_id == user.id:
                    response["data"]["is_leader"] = True
                else:
                    response["data"]["is_leader"] = False

            response = JsonResponse(response, status=200)
            response.set_cookie("username", user.username)
            return response
        else:
            # 登录失败
            return JsonResponse({
                "ret": "error",
                "msg": "登陆失败！请检查你的信息"
            }, status=400)

    except json.JSONDecodeError:
        # 请求数据无法解析
        return JsonResponse({
            "ret": "error",
            "msg": "Invalid JSON data in the request.",
        }, status=400)


def user_logout(request):
    """
    用户退出登录
    GET
    """
    if request.method != "GET":
        return JsonResponse({
            "ret": "error",
            "msg": "Invalid request method"
        }, status=405)

    if request.user.is_authenticated:
        logout(request)
        return JsonResponse({
            "ret": "success",
            "msg": "已退出登录",
        }, status=200)
    else:
        return JsonResponse({
            "ret": "error",
            "msg": "您没有登录",
        }, status=400)


def user_register(request):
    """
    用户注册，创建新的User，CustomUser，并将CustomUser的 user_id 设置为 User 的 id
    POST
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
    @return
    {
        "ret": "success" / "error",
        "msg": "注册成功" / "报错信息"
    }
    """
    if request.method != "POST":
        return JsonResponse({
            "ret": "error",
            "msg": "Invalid request method.",
        }, status=405)

    info = request.params["data"]
    username = info["username"]
    password = info["password"]
    email = info["email"]

    response = {"ret": "error", "msg": None, }

    # 验证用户输入
    if not username or not password or not email:
        response["msg"] = "请输入完整信息"
        return JsonResponse(response, status=400)
    if not is_valid_username(username):
        response["msg"] = "用户名不合法"
        return JsonResponse(response, status=400)
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
        if not user.is_active:
            user.delete()
        else:
            response["msg"] = "用户名已被使用"
            return JsonResponse(response, status=400)
    if User.objects.filter(email=email).exists():
        response["msg"] = "邮箱已被使用"
        return JsonResponse(response, status=400)

    # 创建 User，create_user() 会自动处理密码的加密
    user = User.objects.create_user(username=username, password=password, email=email)
    user.is_active = False
    user.save()

    # TODO 验证码
    token = str(uuid.uuid4()).replace("-", "")
    request.session[token] = user.id
    path = "http://127.0.0.1:8000/user/valid?token={}".format(token)

    subject = "ezctf 激活邮件"
    message = """
           欢迎来到 ezctf！ 
           <br> <a href='{}'>点击激活</a>  
           <br> 若链接不可用，请复制链接到浏览器激活: 
           <br> {}
           <br>                 ezctf 开发团队
           """.format(path, path)
    print("email: " + email)
    result = send_mail(subject=subject, message="", from_email=settings.EMAIL_HOST_USER, recipient_list=[email, ],
                       html_message=message)
    print("result: " + str(result))

    return JsonResponse({
        "ret": "success",
        "msg": "注册成功，请验证后登录",
    }, status=200)


def modify_user_info(request):
    """
    处理用户更新信息
    PUT
    @payload:
    {
        "action":"modify_user_info",
        "data":{
            "old_username": "momoyeyu",
            "new_username": "momoyeyu2",
            "password": "123",
            "new_email": "momoyeyu@outlookcom"
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

    # 获取请求中的数据
    data = request.params["data"]

    # 获取用户
    user = authenticate(request, username=data["old_username"], password=data["password"])

    if user is not None:
        # 用户验证成功
        if data.get("new_username") is not None:
            user.username = data["new_username"]

        if data.get("new_email") is not None:
            user.email = data["new_email"]

        user.save()

        return JsonResponse({
            "ret": "success",
            "msg": "用户信息更新成功"
        })
    else:
        # 用户验证失败
        return JsonResponse({
            "ret": "error",
            "msg": "用户认证失败，无法更新信息"
        })


def del_account(request):
    """
    用户注销账号，删除数据库中与该用户有关的所有数据
    DELETE
    @payload:
    {
        "action":"del_account",
        "data":{
            "username": "momoyeyu",
            "password": "123",
        }
    }
    """
    if request.method != "DELETE":
        return JsonResponse({
            "ret": "error",
            "msg": "Invalid request method.",
        }, status=405)

    if not request.user.is_authenticated:
        return JsonResponse({
            "ret": "error",
            "msg": "用户未登录",
        }, status=403)

    data = request.params["data"]
    username = data["username"]
    password = data["password"]

    # 验证用户身份
    user = authenticate(request, username=username, password=password)
    if user is not None:
        # 删除相关数据，这里以删除用户的自定义数据为例
        try:
            custom_user = CustomUser.objects.get(user_id=user.id)
            team = Team.objects.get(pk=custom_user.team_id)
            if team is not None:
                if team.leader_id == user.id:
                    return JsonResponse({
                        "ret": "error",
                        "msg": "战队队长需要解散战队或转让权限后才能注销"
                    }, status=403)
                else:
                    team.member_count -= 1
                    team.save()
            custom_user.delete()
            user.delete()
        except CustomUser.DoesNotExist:
            pass  # 用户的自定义数据不存在，无需处理

        # 注销用户
        logout(request)

        return JsonResponse({
            "ret": "success",
            "msg": "账号已注销。",
        }, status=204)
    else:
        # 登录失败
        return JsonResponse({
            "ret": "error",
            "msg": "用户名或密码错误。",
        }, status=403)


# def get_user_profile(request):
#     """
#     获取用户数据
#     GET
#     {
#         "action": "user_profile",
#         "user_id": 1
#     }
#     """
#     user_id = request.params["user_id"]
#
#     user = None
#     custom_user = None
#     try:
#         user = User.objects.get(pk=user_id)
#         custom_user = CustomUser.objects.get(user_id=user_id)
#     except ObjectDoesNotExist:
#         return JsonResponse({
#             "ret": "error",
#             "msg": "用户不存在"
#         }, status=404)
#
#     team = None
#     if custom_user.team_id is not None:
#         team = Team.objects.get(pk=custom_user.team_id)
#         is_leader = False
#         if team.leader_id == user_id:
#             is_leader = True
#         return JsonResponse({
#             "ret": "success",
#             "msg": "查询成功",
#             "data": {
#                 "username": user.username,
#                 "score": custom_user.score,
#                 "teamname": team.team_name,
#                 "is_leader": is_leader
#             }
#         }, status=200)
#
#     return JsonResponse({
#         "ret": "success",
#         "msg": "查询成功",
#         "data": {
#             "username": user.username,
#             "score": custom_user.score,
#             "teamname": None,
#             "is_leader": None
#         }
#     }, status=200)


def user_active(request):
    if request.method != "GET":
        return JsonResponse({
            "ret": "error",
            "msg": "Invalid request method.",
        }, status=405)

    token = request.GET.get("token")
    uid = request.session.get(token)
    user = User.objects.get(pk=uid)
    user.is_active = True
    user.save()
    # 创建 CustomUser，关联到 User
    custom_user = CustomUser(user_id=user.id, score=0)
    custom_user.save()
    return JsonResponse({
        "ret": "success",
        "msg": str(user.username) + "的账号已激活"
    }, status=200)



