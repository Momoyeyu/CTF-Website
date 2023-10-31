from django.core.mail import send_mail

from backend import settings
from utils import log_test
from django.test import TestCase
from django.contrib.sessions.middleware import SessionMiddleware
from tasks.models import Task, AnswerRecord
from common.models import CustomUser, Team, Message
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
        self.obj = User.objects.create_user(username='bbb', email='223456789@qq.com', password='123456')
        self.obj = User.objects.create_user(username='ccc', email='323456789@qq.com', password='123456')
        self.obj = User.objects.create_user(username='ddd', email='323456789@qq.com', password='123456')

        self.obj = Team.objects.create(team_name='ez', allow_join=True, member_count=1, leader_id=1)
        self.obj = Team.objects.create(team_name='unez', allow_join=True, member_count=1, leader_id=2)

        self.obj = CustomUser.objects.create(user_id=1, team_id=1, score=0)
        self.obj = CustomUser.objects.create(user_id=2, team_id=2, score=0)
        self.obj = CustomUser.objects.create(user_id=3, team=None, score=0)
        self.obj = CustomUser.objects.create(user_id=4, team_id=1, score=0)

        self.obj = Task.objects.create(task_name='AAA', content='content', flag='aaaa', difficulty=0, points=10,
                                       solve_count=0, task_type=1, annex='aa.txt')
        self.obj = Task.objects.create(task_name='BBB', content='content', flag='bbbb', difficulty=0, points=10,
                                       solve_count=0, task_type=2)

        # self.obj = Message.objects.create(receiver_id=1, origin_id=3, msg="申请加入战队",
        #                                   msg_type=Message.MessageType.APPLICATION.value)

    def test_one(self):
        # self.user_register()
        # send_email()
        self.login()
        self.quit_team()
        self.create_team()
        self.del_team()
        self.search_team()
        self.logout()

    def test_two(self):
        print("===============================")
        self.login_c()
        self.quit_team()
        self.join_team()
        self.join_team()
        self.logout()

        self.login()
        self.verify_apply()
        self.change_team_leader()
        self.logout()

        self.login_c()
        self.quit_team()
        self.logout()

    def test_three(self):
        print("===============================")
        self.login()
        self.invite()
        self.logout()

        self.login_c()
        self.accept()
        self.quit_team()
        self.login_c()

    # user:
    def login(self):
        print("[INFO]: test login: ")
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

    def login_c(self):
        print("[INFO]: test login: ")
        payload = {
            "action": "login",
            "data": {
                "username_or_email": "ccc",
                "password": "123456",
            }
        }
        response = self.client.post('http://localhost/api/common/user', data=payload,
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.client.login(username='ccc', password='123456')
        pprint.pprint(response.json())

    def logout(self):
        print("[INFO]: test logout")
        response = self.client.get('http://localhost/api/common/user?action=logout')
        self.assertEqual(response.status_code, 200)
        self.client.logout()
        pprint.pprint(response.json())

    def user_register(self):
        print("[INFO]: test user register")
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
        self.assertEqual(response.status_code, 200)
        pprint.pprint(response.json())

    # team:
    def create_team(self):
        print("[INFO]: test create team")
        payload = {
            "action": "create_team",
            "data": {
                "leader_name": "aaa",
                "team_name": "ezctf",
                "allow_join": True,
            }
        }
        response = self.client.post('http://localhost/api/common/team', data=json.dumps(payload),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        pprint.pprint(response.json())

    def del_team(self):
        print("[INFO]: test del team")
        payload = {
            "action": "del_team",
            "data": {
                "password": "123456",
            }
        }
        response = self.client.delete('http://localhost/api/common/team?action=del_team', data=json.dumps(payload),
                                      content_type='application/json')
        self.assertEqual(response.status_code, 204)
        if response.status_code == 204:
            # 处理成功的情况，HTTP状态码204表示成功删除
            print("[INFO]: Team deleted successfully")
            print(response.content)
        else:
            # 处理其他状态码或错误情况
            print("[ERROR]: Team deletion failed with status code", response.status_code)
            print(response.content)

    def join_team(self):
        log_test("join team")
        payload = {
            "action": "join_team",
            "data": {
                "team_name": "ez",
            },
        }
        response = self.client.post('http://localhost/api/common/team', data=json.dumps(payload),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        pprint.pprint(response.json())

    def quit_team(self):
        print("[INFO]: test quit team")
        response = self.client.get('http://localhost/api/common/team?action=quit_team')
        pprint.pprint(response.json())

    def search_team(self):
        print("[INFO]: test serach team")
        response = self.client.get('http://localhost/api/common/team?action=search_team&keyword=ez')
        self.assertEqual(response.status_code, 200)
        pprint.pprint(response.json())

    def verify_apply(self):
        log_test("verify apply")
        payload = {
            "action": "verify_apply",
            "data": {
                "applicant": "ccc",
                "accept": True,
            },
        }
        response = self.client.post('http://localhost/api/common/team?action=verify_apply',
                                    data=json.dumps(payload),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        pprint.pprint(response.json())

    def change_team_leader(self):
        log_test("change team leader")
        payload = {
            "action": "change_team_leader",
            "data": {
                "new_leader_name": "ddd",
            },
        }
        response = self.client.put('http://localhost/api/common/team?action=change_team_leader',
                                   data=json.dumps(payload),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        pprint.pprint(response.json())

    def invite(self):
        log_test("invite")
        payload = {
            "action": "invite",
            "data": {
                "invitee": "ccc",  # 受邀用户的用户名
                "invite_msg": "加入我们吧",
            }
        }
        response = self.client.post('http://localhost/api/common/team?action=invite',
                                   data=json.dumps(payload),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        pprint.pprint(response.json())

    def accept(self):
        log_test("accept")
        payload = {
            "action": "accept",
            "data": {
                "inviter": "aaa",
                "accept": True,
            }
        }
        response = self.client.post('http://localhost/api/common/team?action=accept',
                                   data=json.dumps(payload),
                                   content_type='application/json')
        pprint.pprint(response.json())

#
# if __name__ == "__main__":
#     # log_test("user_login()")
#     # test_login()
