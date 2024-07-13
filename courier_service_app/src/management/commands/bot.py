from telebot import TeleBot
from dotenv import load_dotenv
from pathlib import Path
from importlib import reload
from loguru import logger
from django.core.management.base import BaseCommand
import os
# MODULES
import tgbot.management.commands.resources.request as r 
import tgbot.management.commands.resources.markup as m

logger.add(sink='bot.log', format='{time} - {level} - {message}', filter=__name__, level="DEBUG", rotation='100 MB', compression='zip')

dotenv_path = 'PATH/TO/.ENV'
load_dotenv(dotenv_path=dotenv_path)

TGBOT = os.getenv("YOUR_TELEGRAM_TOKEN")
page = None

bot = TeleBot(TGBOT, threaded=False)

payload = {
    'telegram_id': None,
    'first_name': None,
    'phone_number': None,
    'preferred_language': None,
}
def update_language(lang):
    logger.debug('update_language function call')
    m.change_language_ui(lang)
    reload(m)

@bot.message_handler(commands=['start'])
def start(message):
    '''This is START button that calls the funtion for choosing Language'''
    logger.info(f'Start messaging, user: {message.chat.id}')
    response = r.check_courier(message.chat.id)

    if response.status_code != 404:
        logger.info(f'User: {message.chat.id}, was in the database')
        update_language(response.json()['preferred_language'])
        bot.send_message(chat_id=message.chat.id, text=m.WELCOME, reply_markup=m.MAIN_MENU_MARKUP)
    else:
        logger.info(f'User: {message.chat.id}, started registration process')
        bot.send_message(chat_id=message.chat.id, text=m.CHOOSE_LANGUAGE, reply_markup=m.LANGUAGE_MENU_MARKUP)
    
def register(message):
    '''This function call register request'''
    logger.info(f'Final Stage of {message.chat.id} registration, sending gathered information to the server')
    try:
        response = r.register(message, payload)
    except AttributeError:
        bot.send_message(message.chat.id, m.USE_BUTTON)
        sent = bot.send_message(message.chat.id, text=m.SHARE_CONTACT_TEXT, reply_markup=m.SHARE_CONTACT_MARKUP)
        bot.register_next_step_handler(sent, register)
        
    if response.status_code == 201:
        logger.info(f'{message.chat.id}: Registration Successed')
        bot.send_message(chat_id=message.chat.id, text=m.WELCOME, reply_markup=m.MAIN_MENU_MARKUP)
    else:
        logger.warning(f'{message.chat.id}: Registration Unsuccessful, something went wrong')
        bot.send_message(chat_id=message.chat.id, text=m.SOMETHING_WENT_WRONG)

@bot.message_handler(content_types=['text'])
def menu(message):
    global page
    page = 0
    if message.text == m.TAKE_ORDER:
        logger.debug(f'{message.chat.id}, looking for an order')
        orders = r.get_orders(page)
        bot.send_message(message.chat.id, m.TAKEORDERNEW(orders), parse_mode='HTML', reply_markup=m.take_order_btn(orders))

    elif message.text == m.BRANCHES:
        logger.debug(f'{message.chat.id}, branches')
        branches = r.get_branches()
        for branch in branches:
            bot.send_message(message.chat.id, f'<a href="{branch["address_link"]}">{branch["branch_name"]}</a>', parse_mode='HTML')


    elif message.text == m.MY_ORDERS:
        logger.debug(f'{message.chat.id}, MY ORDERS')
        bot.send_message(message.chat.id, text=m.MY_ORDERS, reply_markup=m.MY_ORDERS_MARKUP)
    

    elif message.text == m.ACTIVE:
        orders = r.get_my_active(message.chat.id)
        if len(orders) < 1:
            bot.send_message(message.chat.id, m.EMPTY_ACTIVE)
        else:
            for order in orders:
                sets = r.get_product_set(order['id'])
                product_names = ''
                for set in sets:
                    product = r.get_product(set['product'])
                    product_names += f"{product['name']} ({product['brand']}) - ({set['quantity']}x)\n"
                bot.send_message(message.chat.id, m.ORDER_PRODUCT(order, product_names), parse_mode='HTML', reply_markup=m.done_btn(order["id"]))


    elif message.text == m.HISTORY:
        orders = r.get_my_history(message.chat.id)
        if len(orders) < 1:
            bot.send_message(message.chat.id, m.EMPTY_HISTORY)
        else:
            for order in orders:
                sets = r.get_product_set(order['id'])
                product_names = ''
                for set in sets:
                    product = r.get_product(set['product'])
                    product_names += f"{product['name']} ({product['brand']}) - ({set['quantity']}x)\n"
                bot.send_message(message.chat.id, m.ORDER_PRODUCT(order, product_names), parse_mode='HTML')


    elif message.text == m.SETTINGS:
        bot.send_message(message.chat.id, m.SETTINGS, reply_markup=m.SETTINGS_MENU_MARKUP)


    elif message.text == m.CONNECT_OPERATOR:
        bot.send_contact(message.chat.id, '000000000000', 'NAME', 'SURNAME')
    

    elif message.text == m.CHANGE_LANGUAGE:
        bot.send_message(message.chat.id, m.CHANGE_LANGUAGE, reply_markup=m.LANGUAGE_MENU_MARKUP)
    
    if message.text == m.RUSSIAN:
        logger.info(f'User {message.chat.id}, changed language to RUSSIAN')
        response = r.check_courier(message.chat.id)
        payload['preferred_language'] = 'ru'
        update_language(payload['preferred_language'])

        if response.status_code != 404:
            payload['phone_number'] = response.json()['phone_number']
            r.set_language(message=message, payload=payload)
            bot.send_message(message.chat.id, m.RUSSIAN, reply_markup=m.SETTINGS_MENU_MARKUP)
        else:
            logger.debug(f'User: {message.chat.id}, go through phone number registration')
            sent = bot.send_message(message.chat.id, text=m.SHARE_CONTACT_TEXT, reply_markup=m.SHARE_CONTACT_MARKUP)
            bot.register_next_step_handler(sent, register)

    elif message.text == m.UZBEK:
        logger.info(f'User {message.chat.id}, changed language to UZBEK')
        response = r.check_courier(message.chat.id)
        payload['preferred_language'] = 'uz'
        update_language(payload['preferred_language'])

        if response.status_code != 404:
            payload['phone_number'] = response.json()['phone_number']
            r.set_language(message=message, payload=payload)
            bot.send_message(message.chat.id, m.UZBEK, reply_markup=m.SETTINGS_MENU_MARKUP)
        else:
            logger.debug(f'User: {message.chat.id}, go through phone number registration')
            sent = bot.send_message(chat_id=message.chat.id, text=m.SHARE_CONTACT_TEXT, reply_markup=m.SHARE_CONTACT_MARKUP)
            bot.register_next_step_handler(sent, register)
    

    elif message.text == m.BACK:
        bot.send_message(message.chat.id, m.BACK, reply_markup=m.MAIN_MENU_MARKUP)


@bot.callback_query_handler(func=lambda callback: True)
def callback_order(callback):
    global page
    
    if callback.data.split('-')[0] == 'take':
        bot.answer_callback_query(callback.id, m.ORDER_ACCEPT)
        response = r.take_order(telegram_id=callback.message.chat.id, order_id=callback.data.split('-')[1])
        if response.ok:
            logger.info(f'{callback.message.chat.id} Took Order #{callback.data.split("-")[1]}')
            bot.delete_message(callback.message.chat.id, callback.message.message_id)
            bot.send_message(callback.message.chat.id, m.ORDER_ACCEPTED(callback.data.split("-")[1]), reply_markup=m.MAIN_MENU_MARKUP)

    elif callback.data.split('-')[0] == 'done':
        bot.answer_callback_query(callback.id, m.DONE)
        response = r.finish_delivery(order_id=callback.data.split('-')[1])
        if response.ok:
            logger.info(f'{callback.message.chat.id} Finished Order {callback.data.split("-")[1]}')
            bot.delete_message(callback.message.chat.id, callback.message.message_id)
    
    elif callback.data.split('-')[0] == 'cancel':
        response = r.cancel_order(order_id=callback.data.split('-')[1])
        if response.ok:
            logger.info(f'{callback.message.chat.id} Canceled Order #{callback.data.split("-")[1]}')
            bot.answer_callback_query(callback.id, m.CANCEL)
            bot.delete_message(callback.message.chat.id, callback.message.message_id)

    elif callback.data == 'next':
        bot.answer_callback_query(callback.id, m.FRONT_EM)
        if page < (len(r.get_all_orders()) / 3) - 1:
            page += 1
            orders = r.get_orders(page)
            bot.edit_message_text(text=m.TAKEORDERNEW(orders), chat_id=callback.message.chat.id, message_id=callback.message.message_id, parse_mode='HTML')
            bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=callback.message.message_id, reply_markup=m.take_order_btn(orders))
        
    elif callback.data == 'prev':
        bot.answer_callback_query(callback.id, m.BACK_EM)
        if page > 0:
            page -= 1
            orders = r.get_orders(page)
            bot.edit_message_text(text=m.TAKEORDERNEW(orders), chat_id=callback.message.chat.id, message_id=callback.message.message_id, parse_mode='HTML')
            bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=callback.message.message_id, reply_markup=m.take_order_btn(orders))


class Command(BaseCommand):
  	# Используется как описание команды обычно
    help = 'Implemented to Django application telegram bot setup command'

    def handle(self, *args, **kwargs):
        bot.enable_save_next_step_handlers(delay=2)                 # Сохранение обработчиков
        bot.load_next_step_handlers()								# Загрузка обработчиков
        bot.infinity_polling()										# Бесконечный цикл бота
        