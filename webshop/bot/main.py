from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from .config import TOKEN
from ..db.models import Text, Category, Product, User, Order
from .keyboards import START_KB, PRODUCTS_KB, CART_KB
from .lookups import *


bot = TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):

    if not User.objects.filter(message_chat_id=str(message.chat.id)):
        User.create(message_chat_id=str(message.chat.id),
                    name=message.from_user.first_name,
                    surname=message.from_user.last_name)

    txt = Text.get_text('greetings')
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
    txt = Text.get_text('root_categories')
    bot.send_message(message.chat.id, txt, reply_markup=kb)


@bot.message_handler(content_types=['text'],
                     func=lambda message: message.text == START_KB['discount_products'])
def discount_click(message):
    products = Product.get_discount_products()
    txt = Text.get_text('discount_products')
    bot.send_message(message.chat.id, txt)
    for product in products:
        kb = InlineKeyboardMarkup()
        buttons = [InlineKeyboardButton(PRODUCTS_KB['to_cart'],
                                        callback_data=f'{order_lookup}{separator}{product.id}')]
        kb.add(*buttons)
        if product.discount:
            price_text = f'{product.price} Цена со скидкой - {product.extended_price}'
        else:
            price_text = product.extended_price
        bot.send_photo(message.chat.id, product.image,
                       caption=f'{product.title}\n{product.description}\n{price_text}', reply_markup=kb)


@bot.message_handler(content_types=['text'],
                     func=lambda message: message.text == START_KB['my_cart'])
def cart_click(message):
    user = User.get_user(message_chat_id=str(message.chat.id))
    products = user.cart
    if len(products) == 0:
        txt = Text.get_text('cart_empty')
        bot.send_message(message.chat.id, txt)
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
        button = InlineKeyboardButton(CART_KB['order'], callback_data=f'{cart_lookup}{separator}{cart_checkout}')
        kb.add(button)
        txt = Text.get_text('cart_total') + str(user.cart_total)
        total_message = bot.send_message(message.chat.id, txt, reply_markup=kb)
        user.set_total_message_id(str(total_message.message_id))


@bot.callback_query_handler(func=lambda call: (call.data.split(separator)[0] == cart_lookup and
                                               call.data.split(separator)[1] == cart_checkout))
def checkout(call):
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button = KeyboardButton('Отправить номер телефона', request_contact=True)
    kb.add(button)
    txt = Text.get_text('request_phone')
    bot.send_message(call.message.chat.id, txt, reply_markup=kb)


@bot.message_handler(content_types=['contact'])
def contact(message):
    user = User.get_user(message_chat_id=str(message.chat.id))
    user.save_phone(message.contact.phone_number)
    Order.place_order(user)
    user.empty_cart()
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.add(*[KeyboardButton(text=text) for text in START_KB.values()])
    txt = Text.get_text('cart_checkout')
    bot.send_message(message.chat.id, txt, reply_markup=kb)


@bot.callback_query_handler(func=lambda call: call.data.split(separator)[0] == cart_lookup)
def cart_actions(call):
    user = User.get_user(message_chat_id=str(call.message.chat.id))
    action = call.data.split(separator)[1]
    products = user.cart
    product = Product.objects.get(id=call.data.split(separator)[2])

    if len(products) == 0:
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        txt = Text.get_text('cart_empty')
        bot.send_message(call.message.chat.id, txt)
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

    if user.cart_total == 0:
        txt = Text.get_text('cart_empty')
        bot.edit_message_text(txt, call.message.chat.id, user.total_message_chat_id)
    else:
        kb = InlineKeyboardMarkup()
        button = InlineKeyboardButton(CART_KB['order'], callback_data=f'{cart_lookup}{separator}{cart_checkout}')
        kb.add(button)
        txt = Text.get_text('cart_total') + str(user.cart_total)
        total_message = bot.edit_message_text(txt, call.message.chat.id, user.total_message_chat_id, reply_markup=kb)
        user.set_total_message_id(str(total_message.message_id))


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
        text = Text.get_text('root_categories')
        bot.edit_message_text(text=text, chat_id=call.message.chat.id,
                              message_id=call.message.message_id, reply_markup=kb)

    elif category.is_parent:
        subcategories = category.subcategories
        buttons = [InlineKeyboardButton(cat.title, callback_data=f'{category_lookup}{separator}{cat.id}')
                   for cat in subcategories]
        kb.row(*buttons)

        text = Text.get_text('subcategories').split()
        text.insert(2, category.title)
        text = ' '.join(text)

        if category.has_parent:
            kb.row(InlineKeyboardButton('Назад', callback_data=f'{category_lookup}{separator}{category.parent.id}'))
        elif not category.has_parent:
            kb.row(InlineKeyboardButton('Назад', callback_data=f'{category_lookup}{separator}{root_lookup}'))

        bot.edit_message_text(text=text, chat_id=call.message.chat.id,
                              message_id=call.message.message_id, reply_markup=kb)

    else:
        products = category.get_products()
        txt = Text.get_text('products_text') + str(category.title)
        bot.edit_message_text(text=txt, chat_id=call.message.chat.id, message_id=call.message.message_id)
        for product in products:
            kb = InlineKeyboardMarkup()
            button = InlineKeyboardButton(PRODUCTS_KB['to_cart'],
                                          callback_data=f'{order_lookup}{separator}{product.id}')
            kb.add(button)
            if product.discount:
                price_text = f'{product.price} Цена со скидкой - {product.extended_price}'
            else:
                price_text = product.extended_price
            bot.send_photo(call.message.chat.id, product.image,
                           caption=f'{product.title}\n{product.description}\n{price_text}', reply_markup=kb)


@bot.callback_query_handler(func=lambda call: call.data.split(separator)[0] == order_lookup)
def order_click(call):
    user = User.get_user(message_chat_id=str(call.message.chat.id))
    product = Product.objects.get(id=call.data.split(separator)[1])
    user.add_to_cart(product)
    txt = Text.get_text('cart_added')
    bot.send_message(call.message.chat.id, txt)


def start_bot():
    bot.polling()
