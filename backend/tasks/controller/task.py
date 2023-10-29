from django.http import HttpResponse
from django.http import JsonResponse
from utils import get_request_params, ExceptionEnum, error_template, success_template
from tasks.models import Task, AnswerRecord
from django.contrib.auth.models import User
import traceback


def dispatcher(request):
    action = request.GET.get("action")
    if action == "list_type":
        return list_type(request)
    elif action == "list_all":
        return list_all(request)
    elif action == "query_one":
        return query_one(request)
    else:
        return JsonResponse({"ret": "error", "msg": "Unsupported request!"})


def list_all(request):
    """
    GET
    @param:
    {
        "action": "list_all",
    }
    @return:
    {
        "ret": "success" / "error",
        "msg": "查询成功",
        "data": [
            {
                "task_id": 1,
                "task_name": "ez misc",
                "src": "ezctf",
                "difficulty": 0,
                "points": 10,
                "solve_count": 12,
                "task_type": 0,
            },
            {
                "task_id": 2,
                "task_name": "ez web",
                "src": "ezctf",
                "difficulty": 0,
                "points": 10,
                "solve_count": 12,
                "task_type": 2,
            },
        ]
    }
    """
    if request.method != "GET":
        return error_template(ExceptionEnum.INVALID_REQUEST_METHOD.value, status=405)

    qs = Task.objects.all()
    if not qs:
        return error_template(ExceptionEnum.TEAM_NOT_FOUND.value, status=404)

    task_list = []
    for task in qs:
        task_list.append({
            "task_id": task.id,
            "task_name": task.task_name,
            "src": task.src,
            "difficulty": task.difficulty,
            "points": task.points,
            "solve_count": task.solve_count,
            "task_type": task.task_type,
        })

    return success_template("查询成功", data=task_list, status=200)


def list_type(request):
    """
    GET
    @param:
    {
        "action": "list_task",
        "type": 0,
    }
    @return:
    {
        "ret": "success" / "error",
        "msg": "查询成功",
        "data": [
            {
                "task_id": 1,
                "task_name": "ez web",
                "src": "ezctf",
                "difficulty": 0,
                "points": 10,
                "solve_count": 12,
            },
            {
                "task_id": 2,
                "task_name": "ez web",
                "src": "ezctf",
                "difficulty": 0,
                "points": 10,
                "solve_count": 12,
            },
        ]
    }
    """
    if request.method != "GET":
        return error_template(ExceptionEnum.INVALID_REQUEST_METHOD.value, status=405)

    task_type = request.GET.get("type")
    qs = Task.objects.all()
    if not qs:
        return error_template(ExceptionEnum.TEAM_NOT_FOUND.value, status=404)

    if task_type:
        qs = qs.filter(task_type=int(task_type))  # MISC = 0

    task_list = []
    for task in qs:
        task_list.append({
            "task_id": task.id,
            "task_name": task.task_name,
            "src": task.src,
            "difficulty": task.difficulty,
            "points": task.points,
            "solve_count": task.solve_count,
        })

    return success_template("查询成功", data=task_list, status=200)


def query_one(request):
    """
    GET
    @param:
    {
        "action": "query_one",
        "task_id": 1,
    }
    """
    if request.method != "GET":
        return error_template(ExceptionEnum.INVALID_REQUEST_METHOD.value, status=405)

    task_id = request.GET.get("task_id")
    task = Task.objects.get(pk=task_id)
    if task is None:
        return error_template(ExceptionEnum.TASK_NOT_FOUND.value, status=404)

    # 构建返回的数据
    task_data = {
        "task_id": task.id,
        "task_name": task.task_name,
        "content": task.content,
    }
    return success_template("查询成功", data=task_data)
