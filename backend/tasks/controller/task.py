from django.http import HttpResponse
from django.http import JsonResponse
from utils import get_request_params
from tasks.models import Task,AnswerRecord
from django.contrib.auth.models import User
import traceback

def dispatcher(request):

#    request.params = get_request_params(request)

# = request.params['action']
    action = request.GET.get('action')
    if action == 'list_all':
        return list_task(request)
    elif action == 'query_one':
        return query(request)
    else:
        return JsonResponse({'ret': 1, 'msg': 'Unsupported request!'})


def list_task(request):
    try:
        task_type = request.GET.get('type')
        user_id = request.GET.get('user_id')
        is_login = request.GET.get('is_login')

        qs = Task.objects.all()


        if task_type:
            qs = qs.filter(type=int(task_type))

        task_data = []
        for task in qs:
            is_solved = False
            if is_login == '1':
                # print(is_login)
                user = User.objects.get(id=int(user_id))
                # print(user)
                # print(task)
                is_solved = AnswerRecord.objects.filter(user_id=user_id,task=task).exists()
            print(is_solved)
            task_data.append({
                'task_id' : task.id,
                'task_name': task.task_name,
             #   'src': task.src,
                'difficulty': task.difficulty,
                'points':task.points,
                'solve_count': task.solve_count,
                'is_solved': is_solved,
            })

        return JsonResponse({'ret': 1, 'retlist': task_data, 'total':len(task_data)})

    except:
        return JsonResponse({'ret': 2,  'msg': f'未知错误\n{traceback.format_exc()}'})

def query(request):
    try:
        task_id = request.GET.get('task_id')
        task = Task.objects.get(id=task_id)

        # 构建返回的数据
        task_data = {
            'task_id': task.id,
            'task_name': task.task_name,
            #   'src': task.src,
            'difficulty': task.difficulty,
            'points': task.points,
            'solve_count': task.solve_count,
            'is_solved': is_solved,
        }

        return JsonResponse({'ret': 1, 'data': task_data})

    except:
        return JsonResponse({'ret': 2,  'msg': f'未知错误\n{traceback.format_exc()}'})