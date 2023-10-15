from django.test import TestCase

# Create your tests here.
import requests
import pprint


def test_list_task():

    payload = {
        "action": "list_all",
        "data": {
            "type": "misc",
            "is_login": 1,
            "user_id": 0
        }
    }
    response = requests.get('http://localhost/api/task/list?action=list_all&type=2&is_login=1&user_id=0')
#    response = requests.post('http://localhost/api/task/list', json=payload)

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



if __name__ == "__main__":

    print("test list tasks")
    test_list_task()

    # print("test create team")
    # test_create_team()