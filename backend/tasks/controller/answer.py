import asyncio
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from tasks.models import Task, AnswerRecord
from common.models import CustomUser
from django.contrib.auth.models import User
from django.http import FileResponse
from rank.models import FirstKill
import backend.settings as settings
from django.utils import timezone
import os
from utils import *


def dispatcher(request):
    request.params = get_request_params(request)
    action = request.params["action"]

    if action == "commit_flag":
        return commit_flag(request)
    elif action == "download_attachment":
        return download_attachment(request)
    elif action == "list_solved":
        return list_solved(request)
    elif action == "create_online":
        return create_online(request)
    elif action == "wait_online":
        return wait_online(request)
    elif action == "stop_online":
        return stop_online(request)
    else:
        return error_template(ExceptionEnum.UNSUPPORTED_REQUEST.value, status=405)


@login_required
@require_http_methods("POST")
def commit_flag(request):
    """
    POST
    @payload
    {
        "action" : "commit_flag",
        "data" : {
            "task_id" : 0,
            "flag" : "Flag:abcdefg"
        }
    }
    """
    info = request.params["data"]
    task_id = info["task_id"]
    flag = info["flag"]
    uid = request.session.get("_auth_user_id")
    user = User.objects.get(pk=uid)
    if user is None:
        return error_template(ExceptionEnum.USER_NOT_FOUND.value, status=404)
    task = Task.objects.get(id=task_id)
    if task is None:
        return error_template(ExceptionEnum.TASK_NOT_FOUND.value, status=404)

    cuser = CustomUser.objects.get(user=user)

    if AnswerRecord.objects.filter(user_id=uid, task=task).exists():
        return error_template("重复答题", status=403)
    if task.flag != flag:
        res_data = {
            "task_id": task.id,
            "correct": False,
            "first_kill": False,
        }
        return success_template("WRONG", data=res_data, status=200)
    else:
        cuser.score += task.points
        cuser.save()
        task.solve_count += 1
        task.save()
        cuser.last_answer_time = timezone.now()
        cuser.save()
        AnswerRecord.objects.create(task_id=task_id, user_id=uid, points=task.points)
        res_data = {
            "task_id": task.id,
            "correct": True,
            "first_kill": False,
        }
        if not FirstKill.objects.filter(task_id=task_id).exists():
            FirstKill.objects.create(task_id=task_id, user_id=uid)
            res_data["first_kill"] = True
        return success_template("CORRECT", data=res_data)


@login_required
@require_http_methods("GET")
def download_attachment(request):
    """
    GET
    {
        "action": "download_attachment",
        "task_id": 1,
    }
    """
    task_id = request.GET.get("task_id")
    task = Task.objects.get(pk=task_id)
    if task is None:
        return error_template(ExceptionEnum.TASK_NOT_FOUND.value, status=404)
    if task.annex is None:
        return error_template(ExceptionEnum.DATA_NOT_FOUND.value)
    attach_path = str(task.annex)
    file_path = os.path.join(settings.MEDIA_ROOT, attach_path)

    if os.path.exists(file_path):
        file = open(file_path, "rb")
        response = FileResponse(file)
        response["Content-Type"] = "application/octet-stream"
        response["Content-Disposition"] = f"filename='{os.path.basename(file_path)}'"
        # TODO 关闭文件尚未解决
        return response
    else:
        return error_template(ExceptionEnum.DATA_NOT_FOUND.value, status=404)


def list_solved(request):
    """
    GET
    @param:
    {
        "action": "list_solved",
    }
    @return:
    {
        "ret": "success" / "error",
        "msg": "",
        "data": {
            "solved_list": [0, 2, 3],
        },
    }
    """
    if request.method != "GET":
        return error_template(ExceptionEnum.INVALID_REQUEST_METHOD.value, status=405)

    if not request.user.is_authenticated:
        return error_template(ExceptionEnum.USER_NOT_LOGIN.value, status=403)

    uid = request.session.get("_auth_user_id")
    user = User.objects.get(pk=uid)
    if user is None:
        return error_template(ExceptionEnum.USER_NOT_FOUND.value, status=404)

    answered_tasks = AnswerRecord.objects.filter(user=user)
    task_id_list = []
    for task in answered_tasks:
        task_id_list.append(task.id)
    res_data = {
        "solved_list": task_id_list,
        "total": len(task_id_list),
    }
    return success_template(SuccessEnum.QUERY_SUCCESS.value, data=res_data)

def create_online(request):
    """
    GET
    {
        "action": "create_online",
        "task_id": 1,
    }

    JsonResponse
    {
        'ret': 'success',
        'msg': 'Success!',
        'data':{
            'ip': 'localhost',
            'port': 8478,
        }
    }
    """
    if request.method != "GET":
        return error_template(ExceptionEnum.INVALID_REQUEST_METHOD.value, status=405)

    task_id = request.GET.get("task_id")
    task = Task.objects.get(id=int(task_id))
    print(f'success {task_id}')
    if task is None:
        return error_template(ExceptionEnum.TASK_NOT_FOUND.value, status=404)

    scene_path = os.path.join(settings.ONLINESCENE_ROOT,task.task_name)
    print(scene_path)
    try:
        port = start_container(task.task_name)
        return success_template('Success!', data={'ip': 'localhost', 'port': port,}, status=200)
    except:
        return error_template("Failed to online scene!", status=405)


def wait_online(request):
    """
    GET
    {
        "action": "wait_online",
        "task_id": 2,
    }
    """
    if request.method != "GET":
        return error_template(ExceptionEnum.INVALID_REQUEST_METHOD.value, status=405)

    task_id = request.GET.get("task_id")
    task = Task.objects.get(id=int(task_id))
    # print(f'success {task_id}')
    if task is None:
        return error_template(ExceptionEnum.TASK_NOT_FOUND.value, status=404)

    scene_path = os.path.join(settings.ONLINESCENE_ROOT,task.task_name)
    print(scene_path)
    try:
        asyncio.run(wait_container(task.task_name))
        return success_template('Success!',status=200)
    except:
        return error_template("Failed to online scene!", status=405)
def stop_online(request):
    """
    GET
    {
        "action": "stop_online",
        "task_id": 1,
    }
    """
    if request.method != "GET":
        return error_template(ExceptionEnum.INVALID_REQUEST_METHOD.value, status=405)

    task_id = request.GET.get("task_id")
    task = Task.objects.get(id=int(task_id))
    # print(f'success {task_id}')
    if task is None:
        return error_template(ExceptionEnum.TASK_NOT_FOUND.value, status=404)

    # scene_path = os.path.join(settings.ONLINESCENE_ROOT,task.task_name)
    # print(scene_path)
    try:
        asyncio.run(stop_container(task.task_name))
        return success_template('Success!', status=200)
    except: return error_template("Failed to stop online scene!", status=405)

