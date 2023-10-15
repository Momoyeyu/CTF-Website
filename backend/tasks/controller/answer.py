from django.http import HttpResponse
from django.http import JsonResponse
from common.controller.util import get_request_params
from tasks.models import Task,AnswerRecord
from django.contrib.auth.models import User
import traceback

def dispatcher(request):

    request.params = get_request_params(request)

    action = request.params['action']
    if action == 'list_all':
        return list_task(request)
    elif action == 'query_one':
        return query(request)
    else:
        return JsonResponse({'ret': 1, 'msg': 'Unsupported request!'})


def list_task(request,type):
    try:
        data=request.GET.get('data')
        task_type = data['type']
        user_id = data['user_id']

        qs = Task.objects.all()


        if task_type:
            qs = qs.filter(task_type)

        task_data = []
        for task in qs:
            user = User.objects.get(id=user_id)
            is_solved = AnswerRecord.objects.filter(user=user, task=task).exists()
            task_data.append({
                'task_name': task.task_name,
                'src': task.src,
                'difficulty': task.difficulty,
                'is_solved': is_solved,
            })

        return JsonResponse({'ret': 1, 'retlist': task_data, 'total':len(task_data)})

    except:
        return JsonResponse({'ret': 2,  'msg': f'未知错误\n{traceback.format_exc()}'})

def query(request):

    return JsonResponse()