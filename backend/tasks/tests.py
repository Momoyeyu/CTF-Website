from django.test import TestCase

# Create your tests here.
import requests
import pprint

from django.test import TestCase
from django.urls import reverse

def test_list_task():

    payload = {
        "action": "list_all",
        "data": {
            "type": "misc",
            "is_login": 1,
            "user_id": 0
        }
    }
    response = requests.get('http://localhost/api/task/list?action=list_all&type=2&is_login=1')
#    response = requests.post('http://localhost/api/task/list', json=payload)

    pprint.pprint(response.json())


def test_query():

    response = requests.get('http://localhost/api/task/list?action=query_one&task_id=1')
#    response = requests.post('http://localhost/api/task/list', json=payload)

    pprint.pprint(response.json())



def test_commit_flag():

    payload = {
        "action": "commit_flag",
        "data": {
            "task_id": 2,
            "user_id": 1,
            "flag": "bbbbbbb"
        }
    }

    response = requests.post('http://localhost/api/task/answer', json=payload)

    pprint.pprint(response.json())

def test_download_attachment():

    response = requests.get('http://localhost/api/task/answer?action=download_attachment&task_id=3')

    pprint.pprint(response.headers)
    pprint.pprint(response.text)

if __name__ == "__main__":

    # print("test list tasks:")
    # test_list_task()
    #
    # print("test query one task:")
    # test_query()

    # print("test commit flag:")
    # test_commit_flag()

    print("test download attachment:")
    test_download_attachment()