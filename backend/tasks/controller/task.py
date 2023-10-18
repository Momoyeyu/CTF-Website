from django.http import HttpResponse
from django.http import JsonResponse
from utils import get_request_params
from tasks.models import Task, AnswerRecord
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
    if request.method != 'GET':
        return JsonResponse({
            'ret': 1,
            'msg': 'Unsupported request method.',
        })

    task_type = request.GET.get('type')
    # print("task_type: "+str(task_type))
    # user_id = request.GET.get('user_id')
  #  user_id = request.session.get('_auth_user_id')
    # is_login = request.GET.get('is_login')
    is_login = True
    try:
        user_id = request.session.get('_auth_user_id')
        # print("user_id: "+str(user_id))
    except User.DoesNotExist:
        is_login = False
    try:
        qs = Task.objects.all()
        # print("qs_len:"+str(len(qs)))
        if task_type:
            qs = qs.filter(type=int(task_type))

        # user = User.objects.get(id=int(user_id))

        task_data = []
        for task in qs:
            is_solved = False
            if is_login == True:
                is_solved = AnswerRecord.objects.filter(user_id=user_id,task=task).exists()

            # print("is_solved:", is_solved)

            task_data.append({
                'task_id' : task.id,
                'task_name': task.task_name,
                'src': task.src,
                'difficulty': task.difficulty,
                'points':task.points,
                'solve_count': task.solve_count,
                'is_solved': is_solved,
            })

        return JsonResponse({'ret': 'success', 'retlist': task_data, 'total':len(task_data)})
    except Task.DoesNotExist:
        return JsonResponse({'ret': 'error', 'msg': 'Unsupported request method.'})
    except:
        return JsonResponse({'ret': 'error',  'msg': f'未知错误\n{traceback.format_exc()}'})

def query(request):
    if request.method != 'GET':
        return JsonResponse({
            'ret': 'error',
            'msg': 'Unsupported request method.',
        })

    try:
        task_id = request.GET.get('task_id')
        task = Task.objects.get(id=task_id)

        # 构建返回的数据
        task_data = {
            'task_id': task.id,
            'task_name': task.task_name,
            'content':task.content,
        }
        return JsonResponse({'ret': 0, 'data': task_data})
    except Task.DoesNotExist:
        return JsonResponse({'ret': 1, 'msg': 'Unsupported request method.'})
    except:
        return JsonResponse({'ret': 1,  'msg': f'未知错误\n{traceback.format_exc()}'})