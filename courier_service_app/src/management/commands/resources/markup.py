from telebot import types
from django.utils import translation
from django.utils.translation import gettext as _

def change_language_ui(lang):
    translation.activate(lang)

# Navigation UI
BACK_EM = '\u2B05\uFE0F'
FRONT_EM = '\u27A1\uFE0F'
# Orders UI
ID_EM = '\U0001f194'
LOCATION_PIN_EM = '\U0001f4cd'
TIME_EM = '\U0001f552'
MONEY = '\U0001f4b5'
YES = _('Yes')
NO = _('No')
ORDER_ACCEPT = _('The Order is accepted')

def ORDER_ACCEPTED(order_id):
    return _('Accepted Order:') + f' {order_id}'

def TAKEORDERNEW(orders):
    text = ''
    for order in orders:
        text += f'<strong>{ID_EM}: {order["id"]}</strong>\n\n{LOCATION_PIN_EM}: {order["address"]}\n\n'
    return text

def ORDER_PRODUCT(order, products):
    username = order['username']
    phone = order['userphone']
    price = order['price']
    return f'<strong>{ID_EM}: {order["id"]}</strong>\n\n{products}\n\n{LOCATION_PIN_EM}: {order["address"]}\n\n---------\n{MONEY}: {price} сум\n\n{username}\n<a href="tel:{phone}">{phone}</a>'

# REGISTRATION UI
TELEPHONE_EM = '\u260E\uFE0F'
FLAGRUS_EM = '\U0001f1f7\U0001f1fa'
FLAGUZB_EM = '\U0001f1fa\U0001f1ff'
RUSSIAN = f'Русский {FLAGRUS_EM}'
UZBEK = f'O\'zbekcha {FLAGUZB_EM}'
WELCOME = _('Welcome to Delivery. Here you can take orders and confirm their status.')
CHOOSE_LANGUAGE = f'Выберите язык {FLAGRUS_EM} | Tilni tanlang {FLAGUZB_EM}'
SHARE_CONTACT_TEXT = f'{TELEPHONE_EM} ' + _('Input your number') + ' ' + _('Send contact')
SHARE_CONTACT_BUTTON = f'{TELEPHONE_EM} ' + _('Share Contact')
USE_BUTTON = _('Please, use the button this time')

# MAIN MENU UI
ORDERS_EM = '\U0001f6cd\uFE0F'
MYORDERS_EM = '\U0001f5d2\uFE0F'
BRANCHES_EM = '\U0001f3d8\uFE0F'
SETTINGS_EM = '\u2699\uFE0F'
TAKE_ORDER = f'{ORDERS_EM} ' + _('Take Order')
BRANCHES = f'{BRANCHES_EM} ' + _('Branches')
MY_ORDERS = f'{MYORDERS_EM} ' + _('My Orders')
SETTINGS = f'{SETTINGS_EM} ' + _('Settings')

# SETTINGS UI
GLOBE_EM = '\U0001f310'
PAGER_EM = '\U0001f4df'
CHANGE_LANGUAGE = f'{GLOBE_EM} ' + _('Change Language')
CONNECT_OPERATOR = f'{PAGER_EM} ' + _('Connect with Operator')
BACK = f'{BACK_EM} ' + _('Back')

SOMETHING_WENT_WRONG = _('Something went wrong, please reload the bot')
TAKE_ORDER_INLINE_BUTTON = _('Take Order')

# MY ORDERS UI
GREEN_CIRCLE_EM = '\U0001f7e2'
BOOKS_EM = '\U0001f4da'
CHECK_MARK_EM = '\u2705'
CROSS_MARK_EM = '\u274C'
ACTIVE = f'{GREEN_CIRCLE_EM} ' + _('Active')
HISTORY = f'{BOOKS_EM} '+ _('History')
DONE = f'{CHECK_MARK_EM} ' + _('Done')
CANCEL = f'{CROSS_MARK_EM}'+ _('Cancel')
EMPTY_ACTIVE = _('You don\'t have active orders')
EMPTY_HISTORY = _('Your history is empty')

SHARE_CONTACT_MARKUP = types.ReplyKeyboardMarkup(resize_keyboard=True)
SHARE_CONTACT_MARKUP.row(types.KeyboardButton((SHARE_CONTACT_BUTTON), request_contact=True))

LANGUAGE_MENU_MARKUP = types.ReplyKeyboardMarkup(resize_keyboard=True)
LANGUAGE_MENU_MARKUP.row(types.KeyboardButton(f'Русский {FLAGRUS_EM}'), types.KeyboardButton(f'O\'zbekcha {FLAGUZB_EM}'))

MAIN_MENU_MARKUP = types.ReplyKeyboardMarkup(resize_keyboard=True)
MAIN_MENU_MARKUP.row(types.KeyboardButton(TAKE_ORDER))
MAIN_MENU_MARKUP.row(types.KeyboardButton(MY_ORDERS), types.KeyboardButton(BRANCHES))
MAIN_MENU_MARKUP.row(types.KeyboardButton(SETTINGS))

SETTINGS_MENU_MARKUP = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
SETTINGS_MENU_MARKUP.row(types.KeyboardButton(CHANGE_LANGUAGE),types.KeyboardButton(CONNECT_OPERATOR))
SETTINGS_MENU_MARKUP.row(types.KeyboardButton(BACK))

MY_ORDERS_MARKUP = types.ReplyKeyboardMarkup(resize_keyboard=True)
MY_ORDERS_MARKUP.row(types.KeyboardButton(ACTIVE), types.KeyboardButton(HISTORY))
MY_ORDERS_MARKUP.row(types.KeyboardButton(BACK))

def take_order_btn(orders):
    buttons = []
    for order in orders:
        buttons.append(types.InlineKeyboardButton(text=f'{order["id"]}', callback_data=f'take-{order["id"]}'))
    
    TAKE_ORDER_INLINE_MARKUP = types.InlineKeyboardMarkup([buttons], row_width=3)
    TAKE_ORDER_INLINE_MARKUP.add(types.InlineKeyboardButton(text=BACK_EM, callback_data='prev'), types.InlineKeyboardButton(text=FRONT_EM, callback_data='next'))
    return  TAKE_ORDER_INLINE_MARKUP

def done_btn(order_id):
    DONE_ORDER_MARKUP = types.InlineKeyboardMarkup()
    DONE_ORDER_MARKUP.row(types.InlineKeyboardButton(text=DONE, callback_data=f'done-{order_id}'), types.InlineKeyboardButton(text=CANCEL, callback_data=f'cancel-{order_id}'))
    return DONE_ORDER_MARKUP

def inline_take_order_btn(order_id):
    TAKE_ORDER_MAKE_SURE = types.InlineKeyboardMarkup()
    TAKE_ORDER_MAKE_SURE.row(types.InlineKeyboardButton(text=YES, callback_data=f'yes-{order_id}') ,types.InlineKeyboardButton(text=NO, callback_data='no'))
    return TAKE_ORDER_MAKE_SURE

