import requests
import pprint


def test_del_team():
    payload = {
        "action": "del_team",
        "data": {
            "leader_id": "1",
            "team_name": "ezctf",
        }
    }
    response = requests.delete('http://localhost/api/common/team', json=payload)
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


def test_create_team():
    payload = {
        "action": "create_team",
        "data": {
            "leader_id": "1",
            "team_name": "ezctf",
            "allow_join": "true"
        }
    }
    response = requests.post('http://localhost/api/common/team', json=payload)
    pprint.pprint(response.json())


def log_test(api_name):
    print("[INFO] Testing "+ api_name)


if __name__ == "__main__":

    # log_test("user_login()")
    # test_login()
    #
    # log_test("create_team()")
    # test_create_team()

    log_test("del_team()")
    test_del_team()
