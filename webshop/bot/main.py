from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from .config import TOKEN
from ..db.models import Text, Category, User
from .keyboards import START_KB, PRODUCTS_KB
from .lookups import *

bot = TeleBot(TOKEN)
user = None


@bot.message_handler(commands=['start'])
def start(message):

    if not User.objects.filter(message_chat_id=str(message.chat.id)):
        User.objects.create(message_chat_id=str(message.chat.id),
                            name=message.from_user.first_name,
                            surname=message.from_user.last_name)
    global user
    user = User.objects.get(message_chat_id=str(message.chat.id))

    txt = Text.objects.get(title=Text.TITLES['greetings']).body
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.add(*[KeyboardButton(text=text) for text in START_KB.values()])

    bot.send_message(message.chat.id, txt, reply_markup=kb)


@bot.message_handler(content_types=['text'],
                     func=lambda message: message.text == START_KB['categories'])
def show_categories(message):

    kb = InlineKeyboardMarkup()
    buttons = [InlineKeyboardButton(cat.title, callback_data=f'{category_lookup}{separator}{cat.id}')
               for cat in Category.get_root_categories()]
    kb.add(*buttons)
    bot.send_message(message.chat.id, 'Вот что есть в наличии', reply_markup=kb)


@bot.message_handler(content_types=['text'],
                     func=lambda message: message.text == START_KB['discount_products'])
def discount_click(message):
    bot.send_message(message.chat.id, text='скидки')


@bot.message_handler(content_types=['text'],
                     func=lambda message: message.text == START_KB['my_cart'])
def cart_click(message):
    bot.send_message(message.chat.id, text='корзина')


@bot.callback_query_handler(func=lambda call: call.data.split(separator)[0] == category_lookup)
def category_click(call):

    category_id = call.data.split(separator)[1]
    category = Category.objects.get(id=category_id)
    kb = InlineKeyboardMarkup()

    if category.is_parent:
        subcategories = category.subcategories
        buttons = [InlineKeyboardButton(cat.title, callback_data=f'{category_lookup}{separator}{cat.id}')
                   for cat in subcategories]
        if category.has_parent:
            buttons.append(InlineKeyboardButton('Назад',
                                                callback_data=f'{category_lookup}{separator}{category.parent.id}'))
        kb.add(*buttons)
        bot.edit_message_text(text=f'В категории {category.title} доступны', chat_id=call.message.chat.id,
                              message_id=call.message.message_id, reply_markup=kb)

    else:
        products = category.get_products()
        for product in products:
            kb = InlineKeyboardMarkup()
            buttons = [InlineKeyboardButton(PRODUCTS_KB['order'],
                                            callback_data=f'{product_lookup}{separator}order')]
            kb.add(*buttons)
            bot.send_photo(call.message.chat.id, product.image,
                           caption=f'{product.title}\n{product.description}\n{product.price}')
            bot.send_message(call.message.chat.id, text='Для заказа жми >', reply_markup=kb)

            # удалить кнопку заказа
            # bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)

    # кнопка назад в инлайн клавиатуре переходит к атрибуту парент из текущей категории


"""
@bot.callback_query_handler(func=lambda call: Category.objects.get(title=call.data).is_parent)
def show_subcategories(call):

    kb = InlineKeyboardMarkup()
    buttons = [InlineKeyboardButton(cat.title, callback_data=f'{cat.title}')
               for cat in Category.get_subcategories(call.data)]
    kb.add(*buttons)
    print("CP1")
    bot.edit_message_text(inline_message_id=call.inline_message_id,
                          text=f'В категории {call.data} Доступны такие подкатегории:')
    print("CP1")
    bot.edit_message_reply_markup(inline_message_id=call.inline_message_id,
                                  reply_markup=kb)
    # bot.send_message(call.from_user.id, f'В категории {call.data} Доступны такие подкатегории:', reply_markup=kb)


@bot.callback_query_handler(func=lambda call: not Category.objects.get(title=call.data).is_parent)
def show_products(call):
    category = Category.objects.get(title=call.data)
    products = category.get_products()

    for product in products:
        bot.send_message(call.from_user.id, f'{product.title} - {product.description}')

"""


def start_bot():
    bot.polling()
