import requests
import pprint
from utils import log_test


def test_del_team():
    payload = {
        "action": "del_team",
        "data": {
            "username": "momoyeyu",
            "password": "123",
            "team_name": "ezctf"
        }
    }
    response = requests.delete('http://localhost/api/common/team', json=payload)
    pprint.pprint(response.json())


def test_create_team():
    payload = {
        "action": "create_team",
        "data": {
            "leader_name": "momoyeyu",
            "team_name": "ezctf",
            "allow_join": "true"
        }
    }
    response = requests.post('http://localhost/api/common/team', json=payload)
    pprint.pprint(response.json())


def test_login():
    payload = {
        "action": "login",
        "data": {
            "username_or_email": "momoyeyu",
            "password": "123",
        }
    }
    response = requests.post('http://localhost/api/common/user', json=payload)
    pprint.pprint(response.json())


def test_user_register():
    payload = {
        "action": "register",
        "data": {
            "username": "momoyeyu",
            "password": "123",
            "email": "momoyeyu1@outlook.com",
        }
    }
    response = requests.post('http://localhost/api/common/user', json=payload)
    pprint.pprint(response.json())


def test_logout():
    # Login to get a session
    login_payload = {
        "action": "login",
        "data": {
            "username_or_email": "momoyeyu",
            "password": "123",
        }
    }

    login_response = requests.post('http://localhost/api/common/user', json=login_payload)

    pprint.pprint(login_response.json())
    print("status:", login_response.status_code)

    # Assuming the login was successful, now you can proceed to test the logout.

    if login_response.status_code == 200:
        logout_payload = {
            "action": "logout",
        }

        logout_response = requests.post('http://localhost/api/common/user', json=logout_payload)

        pprint.pprint(logout_response.json())
    else:
        print("Login failed, so cannot test logout.")


if __name__ == "__main__":
    # log_test("user_login()")
    # test_login()

    # 没有用户信息可以跑一下这个来写入信息
    log_test("user_register()")
    test_user_register()

    log_test("logout")
    test_logout()

    # log_test("create_team()")
    # test_create_team()

    # log_test("del_team()")
    # test_del_team()


