from django.test import TestCase

# Create your tests here.
import requests
import pprint

from django.test import TestCase
from django.urls import reverse



def test_rank_user():
    response = requests.get('http://localhost/api/rank/user?action=getrank')
#    response = requests.post('http://localhost/api/task/list', json=payload)

    pprint.pprint(response.json())

def test_rank_team():
    response = requests.get('http://localhost/api/rank/team?action=getrank')
#    response = requests.post('http://localhost/api/task/list', json=payload)

    pprint.pprint(response.json())

if __name__ == "__main__":

    print("test user rank:")
    test_rank_user()

    print("test team rank:")
    test_rank_team()

