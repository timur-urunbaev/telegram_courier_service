import requests
import redis

URL = 'http://172.28.0.2:8000'
client = redis.StrictRedis(host='redis', port=6379, charset="utf-8", decode_responses=True)
token = client.get('token')

########## * COURIER * ##########
def check_courier(telegram_id):
    '''
    check_courier(telegram_id)

    Looking among couriers the one with the same id as given in parameters
    '''

    headers = {
        'Authorization': f'Bearer {token}'
    }

    url = f'{URL}/api/couriers/{telegram_id}'

    response = requests.get(url, headers=headers)
    return response

def register(message, payload):
    '''
    register(message, payload)

    Creating new courier in the database, retrieving information like telegram_id, phone_number, first_name from message
    '''

    payload['telegram_id'] = str(message.chat.id)
    payload['phone_number'] = str(message.contact.phone_number)
    payload['first_name'] = message.from_user.first_name

    headers = {
        'Authorization': f'Bearer {token}'
    }

    url = f'{URL}/api/couriers/'
    
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    if response.status_code != 204:
        return response


def get_orders(page):
    '''
    get_orders(page)

    Getting active orders from the database, takes page parameter, returns 3 Order objects.
    '''
    headers = {
        'Authorization': f'Bearer {token}'
    }

    url = f'{URL}/api/orders/page/{page}'
     
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    if response.status_code != 204:
        return response.json()

def get_all_orders():
    '''
    get_all_orders()

    Getting all active orders from the database, has no parameters
    '''
    headers = {
        'Authorization': f'Bearer {token}'
    }

    url = f'{URL}/api/orders'

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    if response.status_code != 204:
        return response.json()

def get_my_active(telegram_id):
    '''
    get_my_active(telegram_id)

    Looking among active orders those which are correspond to specific courier with the telegram_id that is given as a parameter.
    '''
    headers = {
        'Authorization': f'Bearer {token}'
    }

    url = f'{URL}/api/orders/active/' + f'{telegram_id}'

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    if response.status_code != 204:
        return response.json()

def get_my_history(telegram_id):
    '''
    get_my_history(telegram_id)

    Looking among non-active orders, 5 that are were delivered by specific courier whose telegram_id is given as a parameter.
    '''

    headers = {
        'Authorization': f'Bearer {token}'
    }

    url = f'{URL}/api/orders/history/' + f'{telegram_id}'

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    if response.status_code != 204:
        return response.json()

def take_order(order_id, telegram_id):
    '''
    take_order(order_id, telegram_id)

    Changing the value of Courier in Order from None to Courier with telegram_id given as a parameter.
    '''

    data = {
        'order_id': order_id,
        'telegram_id': telegram_id
    }

    headers = {
        'Authorization': f'Bearer {token}'
    }

    url = f'{URL}/api/orders/takeorder/'

    response = requests.put(url, json=data, headers=headers)
    return response

def cancel_order(order_id):
    '''
    cancel_order(order_id)

    Changing the value of Courier in Order with order_id (given as a parameter), from some Courier to None.
    '''

    data = {
        'order_id': order_id
    }
    
    headers = {
        'Authorization': f'Bearer {token}'
    }

    url = f'{URL}/api/orders/cancel/'

    response = requests.put(url, json=data, headers=headers)
    response.raise_for_status()
    if response.status_code != 204:
        return response

def finish_delivery(order_id):
    '''
    finish_delivery(order_id)

    Changing the value of Order from active to non-active, after delivery is successfully ended.
    '''

    data = {
        'order_id': order_id
    }

    headers = {
        'Authorization': f'Bearer {token}'
    }

    url = f'{URL}/api/orders/finish/'

    response = requests.put(url, json=data, headers=headers)
    response.raise_for_status()
    if response.status_code != 204:
        return response

def get_product_set(order_id):
    '''
    get_product_set(order_id)

    Getting Products that are correspond to specific Order.
    '''

    headers = {
        'Authorization': f'Bearer {token}'
    }

    url = f'{URL}/api/orders/{order_id}/products/'

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    if response.status_code != 204:
        return response.json()
    
def get_product(product_id):

    headers = {
        'Authorization': f'Bearer {token}'
    }

    url = f'{URL}/api/products/{product_id}/'

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    if response.status_code != 204:
        return response.json()
    

def get_branches():
    '''
    get_branches()

    Getting all branches.
    '''
    
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    url = f'{URL}/api/branches/'

    response = requests.get(url=url, headers=headers)
    response.raise_for_status()
    if response.status_code != 204:
        return response.json()


def set_language(message, payload):
    '''
    set_language(message, payload)

    Changing the preferred language of specific Courier
    '''

    payload['telegram_id'] = message.chat.id
    payload['first_name'] = message.from_user.first_name

    headers = {
        'Authorization': f'Bearer {token}'
    }

    url = f'{URL}/api/couriers/{message.chat.id}/'

    return requests.put(url, json=payload, headers=headers)

