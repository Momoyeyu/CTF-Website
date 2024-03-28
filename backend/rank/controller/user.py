from utils import get_request_params, error_template, success_template, ExceptionEnum, SuccessEnum
from common.models import CustomUser


def dispatcher(request):

    action = request.GET.get('action')
    if action == 'rank':
        return user_rank(request)
    else:
        return error_template(ExceptionEnum.UNSUPPORTED_REQUEST.value, status=405)


def user_rank(request):
    """
    @return:
    {
        "ret": "success",
        "msg": "查询成功",
        "data": {
            "user_list": [
                {
                    "username": "aaa",
                    "score": 100,
                    "last_commit": xxx,
                },
                {
                    "username": "bbb",
                    "score": 100,
                    "last_commit": xxx,
                },
            ],
            "total": 2,
        }
    }
    """
    if request.method != 'GET':
        return error_template(ExceptionEnum.INVALID_REQUEST_METHOD.value, status=405)

    users = CustomUser.objects.all()
    user_list = []
    for user in users:
        user_list.append({
            'username': user.user.username,
            'score': user.score,
            'last_commit': user.last_answer_time,
        })
    res_data = {
        "user_list": user_list,
        "total": len(user_list),
    }
    return success_template(SuccessEnum.QUERY_SUCCESS.value, data=res_data)
