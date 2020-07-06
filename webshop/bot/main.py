from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from .config import TOKEN
from webshop.db.models import Text, Category, Product, User
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
    products = Product.get_discount_products()
    for product in products:
        kb = InlineKeyboardMarkup()
        buttons = [InlineKeyboardButton(PRODUCTS_KB['order'],
                                        callback_data=f'{order_lookup}{separator}{product.id}')]
        kb.add(*buttons)
        bot.send_photo(message.chat.id, product.image,
                       caption=f'{product.title}\n{product.description}\n{product.price}', reply_markup=kb)


@bot.message_handler(content_types=['text'],
                     func=lambda message: message.text == START_KB['my_cart'])
def cart_click(message):
    products = user.cart
    if len(products) == 0:
        bot.send_message(message.chat.id, 'В корзине нет товаров')
    else:
        for product in list(set(products)):
            kb = InlineKeyboardMarkup()
            buttons = [
                InlineKeyboardButton("-",
                                     callback_data=f'{cart_lookup}{separator}{cart_minus}{separator}{product.id}'),
                InlineKeyboardButton(f'{products.count(product)}', callback_data='None'),
                InlineKeyboardButton("+",
                                     callback_data=f'{cart_lookup}{separator}{cart_plus}{separator}{product.id}')]
            kb.row(*buttons)
            kb.row(InlineKeyboardButton(
                "убрать", callback_data=f'{cart_lookup}{separator}{cart_remove}{separator}{product.id}'))

            bot.send_message(message.chat.id, f'{product.title}', reply_markup=kb)

        kb = InlineKeyboardMarkup()
        button = InlineKeyboardButton('Заказать', callback_data=f'{cart_lookup}{separator}{cart_checkout}')
        kb.add(button)
        bot.send_message(message.chat.id, 'Для оформления заказа жми', reply_markup=kb)


@bot.callback_query_handler(func=lambda call: (call.data.split(separator)[0] == cart_lookup and
                                               call.data.split(separator)[1] == cart_checkout))
def checkout(call):
    products = user.cart
    if len(products) == 0:
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.send_message(call.message.chat.id, 'В корзине нет товаров')
    else:
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        print(call)


@bot.callback_query_handler(func=lambda call: call.data.split(separator)[0] == cart_lookup)
def cart_actions(call):
    action = call.data.split(separator)[1]
    products = user.cart
    product = Product.objects.get(id=call.data.split(separator)[2])

    if len(products) == 0:
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.send_message(call.message.chat.id, 'В корзине нет товаров')
    elif action == cart_minus and products.count(product) == 1:
        user.minus_cart(product)
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    elif action in [cart_minus, cart_plus]:
        if action == cart_minus:
            user.minus_cart(product)
        elif action == cart_plus:
            user.plus_cart(product)

        kb = InlineKeyboardMarkup()
        buttons = [InlineKeyboardButton("-",
                                        callback_data=f'{cart_lookup}{separator}{cart_minus}{separator}{product.id}'),
                   InlineKeyboardButton(f'{products.count(product)}', callback_data='None'),
                   InlineKeyboardButton("+",
                                        callback_data=f'{cart_lookup}{separator}{cart_plus}{separator}{product.id}')]
        kb.row(*buttons)
        kb.row(InlineKeyboardButton("убрать",
                                    callback_data=f'{cart_lookup}{separator}{cart_remove}{separator}{product.id}'))
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=kb)

    elif action == cart_remove:
        user.remove_from_cart(product)
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

# добавить функцию выбора кол-ва при нажатии на цифру в корзине


@bot.callback_query_handler(func=lambda call: call.data.split(separator)[0] == category_lookup)
def category_click(call):

    lookup = call.data.split(separator)[1]
    kb = InlineKeyboardMarkup()

    if not lookup == root_lookup:
        category = Category.objects.get(id=lookup)

    if lookup == root_lookup:
        buttons = [InlineKeyboardButton(cat.title, callback_data=f'{category_lookup}{separator}{cat.id}')
                   for cat in Category.get_root_categories()]
        kb.add(*buttons)
        text = 'Вот что есть в наличии'
        bot.edit_message_text(text=text, chat_id=call.message.chat.id,
                              message_id=call.message.message_id, reply_markup=kb)

    elif category.is_parent:
        subcategories = category.subcategories
        buttons = [InlineKeyboardButton(cat.title, callback_data=f'{category_lookup}{separator}{cat.id}')
                   for cat in subcategories]
        kb.row(*buttons)
        text = f'В категории {category.title} доступны'

        if category.has_parent:
            kb.row(InlineKeyboardButton('Назад', callback_data=f'{category_lookup}{separator}{category.parent.id}'))
        elif not category.has_parent:
            kb.row(InlineKeyboardButton('Назад', callback_data=f'{category_lookup}{separator}{root_lookup}'))

        bot.edit_message_text(text=text, chat_id=call.message.chat.id,
                              message_id=call.message.message_id, reply_markup=kb)

    else:
        products = category.get_products()

        bot.edit_message_text(text=f'В категории {category.title} доступны следующие товары', chat_id=call.message.chat.id,
                              message_id=call.message.message_id)
        for product in products:
            kb = InlineKeyboardMarkup()
            button = InlineKeyboardButton(PRODUCTS_KB['order'],
                                          callback_data=f'{order_lookup}{separator}{product.id}')
            kb.add(button)
            bot.send_photo(call.message.chat.id, product.image,
                           caption=f'{product.title}\n{product.description}\n{product.price}', reply_markup=kb)


@bot.callback_query_handler(func=lambda call: call.data.split(separator)[0] == order_lookup)
def order_click(call):
    product = Product.objects.get(id=call.data.split(separator)[1])
    user.add_to_cart(product)

    bot.send_message(call.message.chat.id, 'Товар добавлен в корзину')

    # кнопка перехода в корзину/ возврата


def start_bot():
    bot.polling()
