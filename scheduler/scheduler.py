import schedule
import redis
import requests
from loguru import logger
import time

'''
SCHEDULE
--------
This module is needed for automatization of token lifetime processes and data grabbing.
'''

client = redis.StrictRedis(host='redis', port=6379, charset="utf-8", decode_responses=True)
logger.add(sink='schedule.log', format='{time} - {level} - {message}', level="INFO", rotation='100 MB', compression='zip')
URL = 'http://172.28.0.2:8000'

def obtain_pair():
    '''
    obtain_pair
    This method is used to obtain pair of token (access, refresh)
    '''
    url_jwt = f'{URL}/api/token/'

    data = {
        'username': 'root',
        'password': 'admin@29',
    }

    response = requests.post(url=url_jwt, json=data)
    if response.ok:
        logger.info('Token obtain successful')
        data = response.json()
        client.set('token', data['access'])
        client.set('refresh', data['refresh'])
    else:
        logger.warning(f'Token obtain unsuccessful Error {response.status_code}')


def refresh_token():
    '''
    refresh_token
    This method is used to refresh token
    '''
    url_jwt = f'{URL}/api/token/refresh/'

    data = {
        "refresh": client.get('refresh')
    }
    response = requests.post(url=url_jwt, json=data)
    if response.ok:
        logger.info('Token refresh successful')
        data = response.json()
        client.set('token', data['access'])
    else:
        logger.warning(f'Token refesh unsuccessful {response.status_code}')


def grab_data():
    '''
    grab_data
    This method is used for grabbing data from server
    '''
    url = f'{URL}/api/bulavka/orders'
    HEADERS = {
        'Authorization': f'Bearer {client.get("token")}'
    }
    response = requests.get(url=url, headers=HEADERS)
    if response.ok:
        logger.info('Successful Data Mapping')
    else:
        logger.warning(f'Unsuccessful Data Mapping {response.status_code}')

schedule.every(20).seconds.do(obtain_pair)
schedule.every(10).seconds.do(refresh_token)
schedule.every(15).seconds.do(grab_data)

while True:
    schedule.run_pending()
    time.sleep(1)