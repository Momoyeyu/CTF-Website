from django.core.mail import send_mail

from backend import settings
from utils import log_test
from django.test import TestCase
from django.contrib.sessions.middleware import SessionMiddleware
from tasks.models import Task, AnswerRecord
from common.models import CustomUser, Team
from django.contrib.auth.models import User
# Create your tests here.
import requests
import pprint
import json


def send_email():
    print("test send email:")
    path = "http://127.0.0.1:8000/user/valid?token={}".format(123)
    email = "momoyeyu@outlook.com"
    email = "1522384595@qq.com"

    subject = "ezctf 激活邮件"
    message = """
           欢迎来到 ezctf！ 
           <br> <a href='{}'>点击激活</a>  
           <br> 若链接不可用，请复制链接到浏览器激活: 
           <br> {}
           <br>                 ezctf 开发团队
           """.format(path, path)
    result = send_mail(subject=subject, message="", from_email=settings.EMAIL_HOST_USER, recipient_list=[email, ],
                       html_message=message)
    print(result)


class SessionTest(TestCase):
    def setUp(self):
        self.obj = User.objects.create_user(username='aaa', email='123456789@qq.com', password='123456')
        self.obj = User.objects.create_user(username='bbb', email='123456789@qq.com', password='123456')
        self.obj = Team.objects.create(team_name='ez', allow_join=True, member_count=1, leader_id=1)

        self.obj = CustomUser.objects.create(user_id=1, team_id=1, score=0)
        self.obj = CustomUser.objects.create(user_id=2, team_id=1, score=0)

        self.obj = Task.objects.create(task_name='AAA', content='content', flag='aaaa', difficulty=0, points=10,
                                       solve_count=0, type=2, annex='aa.txt')
        self.obj = Task.objects.create(task_name='BBB', content='content', flag='bbbb', difficulty=0, points=10,
                                       solve_count=0, type=2)

    def test_main(self):
        self.user_register()
        # send_email()
        self.login()

        self.create_team()
        self.search_team()
        # self.del_team()

        self.logout()

        self.create_team()
        self.search_team()

    def login(self):
        print("test login: ")
        payload = {
            "action": "login",
            "data": {
                "username_or_email": "aaa",
                "password": "123456",
            }
        }
        response = self.client.post('http://localhost/api/common/user', data=payload,
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.client.login(username='aaa', password='123456')
        pprint.pprint(response.json())

    def list_task(self):
        print("test list task: ")
        # 创建一个测试客户端
        client = self.client

        # 发起请求，检查 session 中的值
        response = client.get('http://localhost/api/task/list?action=list_all&type=2')  # 替换为实际的 URL
        pprint.pprint(response.json())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client.session.get('user_id'), None)  # 检查 session 中的值

    def commit_flag(self):
        print("test commit flag: ")

        # users = User.objects.all()
        # for user in users:
        #     print("--user_id: "+str(user.id))

        payload = {
            "action": "commit_flag",
            "data": {
                "task_id": 1,
                "user_id": 1,
                "flag": "aaaa"
            }
        }

        response = self.client.post('http://localhost/api/task/answer', data=payload, content_type='application/json')
        pprint.pprint(response.json())

    def rank_user(self):
        print("test rank user: ")
        response = self.client.get('http://localhost/api/rank/user?action=getrank')
        pprint.pprint(response.json())

    def rank_team(self):
        print("test rank team: ")
        response = self.client.get('http://localhost/api/rank/team?action=getrank')
        pprint.pprint(response.json())

    def query_one(self):
        print("test query one task: ")
        response = self.client.get('http://localhost/api/task/list?action=query_one&task_id=1')
        pprint.pprint(response.json())

    def download_attachment(self):
        print("test download attachment: ")
        response = self.client.get('http://localhost/api/task/answer?action=download_attachment&task_id=1')
        pprint.pprint(response.headers)
        # pprint.pprint(response)

    def del_team(self):
        payload = {
            "action": "del_team",
            "data": {
                "username": "aaa",
                "password": "123456",
            }
        }
        response = self.client.delete('http://localhost/api/common/team', data=json.dumps(payload),
                                      content_type='application/json')
        pprint.pprint(response.json())

    def create_team(self):
        payload = {
            "action": "create_team",
            "data": {
                "leader_name": "aaa",
                "team_name": "ezctf",
                "allow_join": "true"
            }
        }
        response = self.client.post('http://localhost/api/common/team', data=json.dumps(payload),
                                    content_type='application/json')
        pprint.pprint(response.json())

    def user_register(self):
        payload = {
            "action": "register",
            "data": {
                "username": "momoyeyu",
                "password": "123",
                "email": "momoyeyu@outlook.com",
            }
        }
        response = self.client.post('http://localhost/api/common/user', data=json.dumps(payload),
                                    content_type='application/json')
        pprint.pprint(response.json())

    def search_team(self):
        response = self.client.get('http://localhost/api/common/team?action=search_team&keyword=ez')
        pprint.pprint(response.json())

    def logout(self):
        logout_response = self.client.get('http://localhost/api/common/user?action=logout')

        pprint.pprint(logout_response.json())

#
# if __name__ == "__main__":
#     # log_test("user_login()")
#     # test_login()
#
#     # 没有用户信息可以跑一下这个来写入信息
#     log_test("user_register()")
#     test_user_register()
#
#     log_test("logout")
#     test_logout()
#
#     # log_test("create_team()")
#     # test_create_team()
#
#     # log_test("del_team()")
#     # test_del_team()
