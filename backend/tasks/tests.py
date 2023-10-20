from django.test import TestCase
from django.contrib.sessions.middleware import SessionMiddleware
from tasks.models import Task, AnswerRecord
from common.models import CustomUser, Team
from django.contrib.auth.models import User
# Create your tests here.
import requests
import pprint
from django.urls import reverse

class SessionTest(TestCase):
    def setUp(self):
        self.obj = User.objects.create_user(username='aaa', email='123456789@qq.com',password='123456')
        self.obj = User.objects.create_user(username='bbb', email='123456789@qq.com', password='123456')
        self.obj = Team.objects.create(team_name='ez', allow_join=True, member_count=1, leader_id=1)

        self.obj = CustomUser.objects.create(user_id=1, team_id=1, score=0)
        self.obj = CustomUser.objects.create(user_id=2, team_id=1, score=0)

        self.obj = Task.objects.create(task_name='AAA', content='content', flag='aaaa', difficulty=0, points=10, solve_count=0, type=2, annex='aa.txt')
        self.obj = Task.objects.create(task_name='BBB', content='content', flag='bbbb', difficulty=0, points=10, solve_count=0, type=2)

    def test_main(self):
        self.login()
        self.list_task()
        self.query_one()
        self.download_attachment()
        self.commit_flag()
        self.list_task()
        self.rank_user()
        self.rank_team()

    def login(self):
        print("test login: ")
        payload = {
            "action": "login",
            "data": {
                "username_or_email": "aa",
                "password": "123456",
            }
        }
        # 模拟登录，设置 session 数据
        #  session_middleware = SessionMiddleware()
        #  session_middleware.process_request(self)
        response = self.client.post('http://localhost/api/common/user', data=payload, content_type='application/json')
    #    self.assertEqual(response.status_code, 200)
        self.client.login(username='aa', password='123456')
        pprint.pprint(response.json())

    def list_task(self):
        print("test list task: ")
        client = self.client
        response = client.get('http://localhost/api/task/list?action=list_all&type=2')
        pprint.pprint(response.json())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client.session.get('user_id'), None)

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
        # pprint.pprint(response.content_params)
