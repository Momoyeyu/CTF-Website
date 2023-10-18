from django.http import HttpResponse
from django.http import JsonResponse
from utils import get_request_params
from tasks.models import Task, AnswerRecord
from common.models import CustomUser
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.http import FileResponse
from rank.models import FirstKill
import backend.settings as settings
from django.utils import timezone
import os
import traceback

def dispatcher(request):

    if request.method == 'POST':
        request.params = get_request_params(request)
        action = request.params['action']
    else:
        action = request.GET.get('action')

    if action == 'commit_flag':
        return commit_flag(request)
    elif action == 'download_attachment':
        return download_attachment(request)
    else:
        return JsonResponse({'ret': 1, 'msg': 'Unsupported request!'})


def commit_flag(request):
    """
    Need info:
    {
        "action" : "commit_flag",
        "data" : {
            "task_id" : 0,
            "flag" : "Flag:abcdefg"
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
        task_id = info['task_id']
        flag = info['flag']
        user_id = request.session.get('_auth_user_id')
        task = Task.objects.get(id=task_id)
        cuser = CustomUser.objects.get(user_id=user_id)

        if task.flag != flag:
            return JsonResponse({'ret': 1,  'msg': 'Wrong!'})
        elif AnswerRecord.objects.filter(user_id=user_id,task=task).exists():
            return JsonResponse({'ret': 1, 'msg': '重复答题!'})
        else:
            cuser.score += task.points
            cuser.save()
            task.solve_count += 1
            task.save()
            cuser.last_answer_time = timezone.now()
            cuser.save()
            record = AnswerRecord.objects.create(task_id=task_id, user_id=user_id, points=task.points)
            if FirstKill.objects.filter(task_id=task_id).exists() == False:
                FirstKill.objects.create(task_id=task_id,user_id=user_id)
                return JsonResponse({'ret': 0, 'msg': f'First Killed! Add a new record {record.id}.'})
            return JsonResponse({'ret': 0, 'msg':f'Accepted! Add a new record {record.id}.'})
    except Task.DoesNotExist:
        return JsonResponse({'ret': 1, 'msg' : 'Question not found.'}, status=404)
    except CustomUser.DoesNotExist:
        return JsonResponse({'ret':1, 'msg': 'User not found.'}, status=404)
    except:
        return JsonResponse({'ret': 1,  'msg': f'未知错误\n{traceback.format_exc()}'},status=404)

def download_attachment(request):
    """
    need info:task_id
    """
    if request.method != 'GET':
        return JsonResponse({
            'ret': 'error',
            'msg': 'Unsupported request method.',
        })
    try:
        task_id = request.GET.get('task_id')

        # print(task_id)
        task = Task.objects.get(id=int(task_id))

        attach_path = str(task.annex)
        file_path = os.path.join(settings.MEDIA_ROOT, attach_path)

        if os.path.exists(file_path):
            file = open(file_path, 'rb')
            response = FileResponse(file)
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = f'filename="{os.path.basename(file_path)}"'
            # TODO 关闭文件尚未解决
            return response
        else:
            return HttpResponse('File not found', status=404)
    except Task.DoesNotExist:
        return HttpResponse('Task not found', status=404)
    except:
        return HttpResponse(f'未知错误\n{traceback.format_exc()}', status=404)