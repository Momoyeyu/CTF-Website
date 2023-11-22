from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from backend import settings
from utils import get_request_params, is_valid_username, error_template, success_template, send_message, generate
from utils import ExceptionEnum, SuccessEnum
from django.contrib.auth.models import User
from common.models import CustomUser, Team, Message
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods


"""
此文件仅处理 user表 数据
"""


def dispatcher(request):
    # 将请求参数统一放入request 的 params 属性中，方便后续处理
    request.params = get_request_params(request)
    # print("\n=====\n", request, "\n=====\n")
    # print("\n=====\n", request.params, "\n=====\n")

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
    elif action == "forget_password":
        return forget_password(request)
    elif action == "reset_password":
        return reset_password(request)
    elif action == "user_active":
        return user_active(request)

    else:
        return error_template(ExceptionEnum.UNSUPPORTED_REQUEST.value, status=405)


@require_http_methods("POST")
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
            "is_leader": true
        }
    }
    """
    if request.method != "POST":
        return error_template(ExceptionEnum.INVALID_REQUEST_METHOD.value, status=405)

    info = request.params["data"]
    username_or_email = info["username_or_email"]
    password = info["password"]

    if "@" in username_or_email:
        user = authenticate(request, email=username_or_email, password=password)
    else:
        user = authenticate(request, username=username_or_email, password=password)

    if user is None:
        return error_template("登陆失败！请检查你的信息", status=403)

    if user.is_active is False:
        return error_template("用户未激活", status=403)
    custom_user = CustomUser.objects.get(user_id=user.id)
    if custom_user is None:
        return error_template("用户未激活", status=403)
    login(request, user)
    request.session['username'] = user.username
    request.session['_auth_user_id'] = user.id

    res_data = {
        "username": user.username,
        "score": custom_user.score,
        "team_name": None,
        "is_leader": False,
    }

    if custom_user.team_id is not None:
        team = Team.objects.get(pk=custom_user.team_id)
        res_data["team_name"] = team.team_name
        if team.leader_id == user.id:
            res_data["is_leader"] = True
        else:
            res_data["is_leader"] = False

    return success_template("登录成功", data=res_data)


@require_http_methods("GET")
@login_required
def user_logout(request):
    """
    用户退出登录
    GET
    """
    if request.method != "GET":
        return error_template(ExceptionEnum.INVALID_REQUEST_METHOD.value, status=405)
    if request.user.is_authenticated:
        del request.session['_auth_user_id']
        logout(request)
        return success_template("已退出登录")
    else:
        return error_template(ExceptionEnum.USER_NOT_LOGIN.value, status=403)


@require_http_methods("POST")
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
        }
    }
    @return
    {
        "ret": "success" / "error",
        "msg": "注册成功" / "报错信息"
    }
    """
    if request.method != "POST":
        return error_template(ExceptionEnum.INVALID_REQUEST_METHOD.value, status=405)

    info = request.params["data"]
    username = info["username"]
    password = info["password"]
    email = info["email"]

    # 验证用户输入
    if not username or not password or not email:
        return error_template("请输入完整信息", status=400)
    if not is_valid_username(username):
        return error_template("用户名含有非法字符", status=400)
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
        if not user.is_active:
            user.delete()
        else:
            return error_template(ExceptionEnum.NAME_EXIST.value, status=409)
    if User.objects.filter(email=email).exists():
        user = User.objects.get(email=email)
        if not user.is_active:
            user.delete()
        else:
            return error_template("邮箱已被使用", status=409)

    # 创建 User，create_user() 会自动处理密码的加密
    user = User.objects.create_user(username=username, password=password, email=email)
    user.is_active = False

    valid_code = generate(5)

    subject = "ezctf 激活邮件"
    message = """
              您的验证码：<p style="font-weight: bold;">{}</p>
              <br> 
              <br>             ezctf 开发团队
              """.format(valid_code)
    result = send_mail(subject=subject, message="", from_email=settings.EMAIL_HOST_USER, recipient_list=[email, ],
                       html_message=message)
    user.first_name = valid_code
    user.save()
    res_data = {"username": user.username, }
    return success_template("注册成功，请验证后登录", data=res_data)


@require_http_methods("PUT")
@login_required
def modify_user_info(request):
    """
    处理用户更新信息
    PUT
    @payload:
    {
        "action": "modify_user_info",
        "data": {
            "new_username": "momoyeyu2",
            "password": "123",
        }
    }
    """
    if request.method != "PUT":
        return error_template(ExceptionEnum.INVALID_REQUEST_METHOD.value, status=405)

    if not request.user.is_authenticated:
        return error_template(ExceptionEnum.USER_NOT_LOGIN.value, status=403)

    # 获取请求中的数据
    data = request.params["data"]
    new_username = str(data["new_username"])
    password = data["password"]
    uid = request.session.get('_auth_user_id')

    # 检查数据合法性
    if new_username.isspace():
        return error_template("用户名不能为空", status=400)

    if not is_valid_username(new_username):
        return error_template("用户名含有非法字符", status=400)

    # 获取用户
    user = User.objects.get(pk=uid)
    if user is None:
        return error_template(ExceptionEnum.USER_NOT_FOUND.value, status=404)
    user = authenticate(request, username=user.username, password=password)
    if user is None:
        return error_template(ExceptionEnum.WRONG_PASSWORD.value, status=403)

    user.username = new_username
    user.save()

    res_data = {"new_username": user.username, }
    return success_template("用户信息更新成功", data=res_data, status=200)


@require_http_methods("DELETE")
@login_required
def del_account(request):
    """
    用户注销账号，删除数据库中与该用户有关的所有数据
    DELETE
    @payload:
    {
        "action":"del_account",
        "data":{
            "password": "123",
        }
    }
    """
    if request.method != "DELETE":
        return error_template(ExceptionEnum.INVALID_REQUEST_METHOD.value, status=405)

    if not request.user.is_authenticated:
        return error_template(ExceptionEnum.USER_NOT_LOGIN.value, status=403)

    data = request.params["data"]
    password = data["password"]
    uid = request.session.get('_auth_user_id')
    user = User.objects.get(pk=uid)
    if user is None:
        return error_template(ExceptionEnum.USER_NOT_FOUND.value, status=404)
    # 验证用户身份
    user = authenticate(request, username=user.username, password=password)
    if user is None:
        return error_template(ExceptionEnum.WRONG_PASSWORD.value, status=403)

    # 删除相关数据，这里以删除用户的自定义数据为例
    custom_user = CustomUser.objects.get(user=user)
    if custom_user is None:
        return error_template(ExceptionEnum.USER_NOT_FOUND.value, status=404)

    team = None
    if custom_user.team is not None:
        team = Team.objects.get(pk=custom_user.team_id)
    if team is not None:
        if team.leader == user:  # is leader
            teammates = CustomUser.objects.filter(team=team)
            new_leader = teammates.first()
            if new_leader is None:  # 没有队员，战队自动删除
                team.delete()
            else:  # 有队员，队长自动分配给队员
                msg = str(user.username + "将战队转交给了" + new_leader.user.username)
                for each in teammates:
                    send_message(new_leader.user.id, each.user.id, msg,
                                 msg_type=Message.MessageType.CHAT.value)  # CHAT = 1
                team.leader_id = new_leader.user.id
                team.member_count -= 1
                team.save()
        else:  # not leader
            team.member_count -= 1
            team.save()

    # 注销用户
    logout(request)
    custom_user.delete()
    user.delete()

    return success_template("账号已注销", status=204)


@require_http_methods("POST")
def user_active(request):
    """
    POST
    {
        "action": "user_active",
        "data": {
            "username": "momoyeyu",
            "valid_code": "65535",
        },
    }
    """
    if request.method != "POST":
        return error_template(ExceptionEnum.INVALID_REQUEST_METHOD.value, status=405)

    data = request.params["data"]
    username = data["username"]
    valid_code = data["valid_code"]
    if not valid_code or not username:
        return error_template(ExceptionEnum.MISS_PARAMETER.value, status=400)
    user = User.objects.get_by_natural_key(username)
    if user is None:
        return error_template(ExceptionEnum.USER_NOT_FOUND.value, status=404)
    if user.first_name != valid_code:
        user.first_name = ""
        user.save()
        return error_template("验证码错误", status=403)
    user.first_name = ""
    user.is_active = True
    user.save()
    # 创建 CustomUser，关联到 User
    custom_user = CustomUser(user_id=user.id, score=0)
    custom_user.save()
    return success_template("账号已激活", status=200)


@require_http_methods("POST")
def forget_password(request):
    """
    POST
    {
        "action": "forget_password",
        "data": {
            "email": "momoyeyu@outlook.com",
        }
    }
    """
    if request.method != "POST":
        return error_template(ExceptionEnum.INVALID_REQUEST_METHOD.value, status=405)
    data = request.params["data"]
    email = data["email"]
    user = User.objects.get(email=email)
    if user is None or user.is_active is False:
        return error_template(ExceptionEnum.USER_NOT_FOUND.value, status=404)
    valid_code = generate(5)

    subject = "ezctf 重置密码"
    message = """
              您的验证码：<p style="font-weight: bold;">{}</p>
              <br> 
              <br>             ezctf 开发团队
              """.format(valid_code)
    result = send_mail(subject=subject, message="", from_email=settings.EMAIL_HOST_USER, recipient_list=[email, ],
                       html_message=message)
    user.first_name = valid_code
    user.save()
    return success_template(SuccessEnum.REQUEST_SUCCESS.value)


@require_http_methods("PUT")
def reset_password(request):
    """
    PUT
    {
        "action": "reset_password",
        "data":{
            "valid_code": "65535",
            "email": "momoyeyu@outlook.com",
            "new_password": "123",
        }
    }
    """
    if request.method != "PUT":
        return error_template(ExceptionEnum.INVALID_REQUEST_METHOD.value, status=405)
    data = request.params["data"]
    valid_code = data["valid_code"]
    new_password = data["new_password"]
    email = data["email"]
    user = User.objects.get(email=email)
    if user is None:
        return error_template(ExceptionEnum.USER_NOT_FOUND.value, status=404)
    if user.first_name != valid_code:
        user.first_name = ""
        user.save()
        return error_template("验证码错误", status=403)
    user.set_password(new_password)
    user.first_name = ""
    user.save()

    return success_template(SuccessEnum.MODIFICATION_SUCCESS.value)
