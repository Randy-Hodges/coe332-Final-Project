

import json
import os
import re
import time

import pytest
import requests


api_host = 'localhost'
api_port = '5000'
api_prefix = f'http://{api_host}:{api_port}'


def test_info():
    route = f'{api_prefix}/'
    response = requests.get(route)

    assert response.ok == True
    assert response.status_code == 200
    assert bool(re.search('Try the following routes', response.text)) == True


def test_data_upload():
    route = f'{api_prefix}/data'
    response = requests.post(route)

    assert response.ok == True
    assert response.status_code == 200
    assert response.content == b'Data has been loaded to Redis from file\n'


def test_jobs_info():
    route = f'{api_prefix}/jobs'
    response = requests.get(route)

    assert response.ok == True
    assert response.status_code == 200
    assert bool(re.search('To submit a job,', response.text)) == True


def test_jobs_cycle():
    route = f'{api_prefix}/jobs/wind-speed'
    response = requests.get(route)

    assert response.ok == True
    assert response.status_code == 200

    UUID = response.json()['id']
    assert isinstance(UUID, str) == True
    assert response.json()['status'] == 'submitted'

    time.sleep(15)
    route = f'{api_prefix}/jobs/{UUID}'
    response = requests.get(route)

    assert response.ok == True
    assert response.status_code == 200

    assert response.json()['status'] == 'complete'

