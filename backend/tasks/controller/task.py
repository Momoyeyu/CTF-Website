from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from utils import get_request_params, ExceptionEnum, error_template, success_template, SuccessEnum
from tasks.models import Task, AnswerRecord
from django.contrib.auth.models import User


def dispatcher(request):
    action = request.GET.get("action")
    if action == "list":
        return list_tasks(request)
    elif action == "detail":
        return detail(request)
    else:
        return error_template(ExceptionEnum.UNSUPPORTED_REQUEST.value, status=405)


@require_http_methods("GET")
def list_tasks(request):
    """
    GET
    @param:
    {
        "action": "list",
        "type": 0,
    }
    @return:
    {
        "ret": "success" / "error",
        "msg": "查询成功",
        "data": {
            "task_list": [
                {
                    "task_id": 1,
                    "task_name": "ez web",
                    "src": "ezctf",
                    "difficulty": 0,
                    "points": 10,
                    "solve_count": 12,
                    "solved": true,
                },
                {
                    "task_id": 2,
                    "task_name": "ez web",
                    "src": "ezctf",
                    "difficulty": 0,
                    "points": 10,
                    "solve_count": 12,
                    "solved": false,
                },
            ]
        "total": 2,
    }
    """
    task_type = int(request.GET.get("type"))
    print("task_type", task_type)
    tasks = find_by_type_and_difficulty(task_type=task_type)

    user = None
    if request.user.is_authenticated:
        uid = request.session.get('_auth_user_id')
        user = User.objects.get(pk=uid)

    dic = {}
    for task in tasks:
        dic[task.id] = False

    if user is not None:
        answered_tasks = AnswerRecord.objects.filter(user=user)
        for solved_task in answered_tasks:
            dic[solved_task.task_id] = True

    task_list = []
    for task in tasks:
        solved = dic[task.id]
        task_list.append({
            "task_id": task.id,
            "task_name": task.task_name,
            "src": task.src,
            "difficulty": task.difficulty,
            "points": task.points,
            "solve_count": task.solve_count,
            "task_type": task.task_type,
            "solved": solved,
        })

    res_data = {
        "task_list": task_list,
        "total": len(task_list),
    }

    return success_template(SuccessEnum.QUERY_SUCCESS.value, data=res_data, status=200)


@login_required
@require_http_methods("GET")
def detail(request):
    """
    GET
    @param:
    {
        "action": "detail",
        "task_id": 1,
    }
    """
    task_id = request.GET.get("task_id")
    if not task_id:
        return error_template(ExceptionEnum.MISS_PARAMETER.value, status=400)
    task = Task.objects.get(pk=task_id)
    if task is None:
        return error_template(ExceptionEnum.TASK_NOT_FOUND.value, status=404)

    # 构建返回的数据
    res_data = task_data_format(task)
    return success_template(SuccessEnum.QUERY_SUCCESS.value, data=res_data)


#####################
#      Service      #
#####################

def find_by_type_and_difficulty(task_type=-1, difficulty=-1):
    """
    class TaskType(models.IntegerChoices):
        MISC = 0
        CRYPTO = 1
        WEB = 2
        REVERSE = 3
        PWN = 4

    class Difficulty(models.IntegerChoices):
        EAZY = 0
        Medium = 1
        HARD = 2
    """
    filter_type = False
    filter_diff = False
    if task_type in range(0, 5):
        print("in range")
        filter_type = True
    else:
        print("out range")
    if int(difficulty) in range(0, 3):
        filter_diff = True
    if filter_type and filter_diff:
        return Task.objects.filter(task_type=task_type, difficulty=difficulty)
    elif filter_type:
        return Task.objects.filter(task_type=task_type)
    elif filter_diff:
        return Task.objects.filter(difficulty=difficulty)
    else:
        return Task.objects.all()


def task_data_format(task):
    flag = task.annex is not None
    return {
        "task_id": task.id,
        "task_name": task.task_name,
        "annex": flag,
        "content": task.content,
        "task_type": task.task_type,
    }
