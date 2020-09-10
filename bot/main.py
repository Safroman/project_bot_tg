from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from config import TOKEN, RATES, WALLETS
from contents import *
from models import *
import datetime
import time
import copy
import logging


bot = TeleBot(TOKEN)
logging.basicConfig(format='%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG, filename='bot_log.log')


@bot.message_handler(commands=['start'])
def start(message):

    if Users.objects.filter(user_id=str(message.chat.id)):
        cb = f'initiate{SP}existing'
    else:
        if len(message.text.split()) > 1:
            cb = f'initiate{SP}{message.text.split()[1]}'
        else:
            cb = f'initiate{SP}new'

    kb = InlineKeyboardMarkup()
    kb.add(*[InlineKeyboardButton(LANGUAGE_KB[code], callback_data=f'{cb}{SP}{code}') for code in LANGUAGE_KB.keys()])

    bot.send_message(message.chat.id, 'Выберите язык / Choose your language', reply_markup=kb)


@bot.callback_query_handler(func=lambda call: call.data.split(SP)[0] == 'initiate')
def initiate(call):

    lang = call.data.split(SP)[-1]
    if call.data.split(SP)[1] == 'existing' \
            and len(Users.objects.filter(user_id=str(call.message.chat.id))) >= 1:
        user = Users.get_user(user_id=str(call.message.chat.id))

        if user.lang != lang:
            user.set_language(lang)

    else:
        trial = Payments.create(user_id=str(call.message.chat.id),
                                payment_type='trial',
                                confirmed=1)
        user = Users.create(user_id=str(call.message.chat.id),
                            user_name=call.from_user.username,
                            language=lang,
                            current_payment=trial,
                            referrals=[])
        user.gen_ref_link()

        if call.data.split(SP)[1] != 'new':
            referrer = Users.objects.get(id=call.data.split(SP)[1])
            referrer.add_referral(user)
        else:
            pass

    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    kb.add(*[KeyboardButton(text=START_KB_PICS[button] + ' ' + START_KB[button][user.lang])
             for button in START_KB.keys()])

    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    bot.send_message(call.message.chat.id, GREETINGS[user.lang], reply_markup=kb, parse_mode='markdown')
    bot.send_message(call.message.chat.id, GREETINGS_2[user.lang], parse_mode='markdown')


"""
Account
"""


def f_price(price):
    p = str(price).split('.')
    if len(p[0]) > 1:
        return '.'.join([p[0], p[1][0:2]])
    else:
        return '.'.join([p[0], p[1][0:5]])


@bot.message_handler(content_types='text', func=lambda message: message.text.split()[-1] in START_KB['account'].values())
def show_account(message):

    user = Users.get_user(user_id=str(message.chat.id))

    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(*[InlineKeyboardButton(text=ACCOUNT_PICS[button] + text[user.lang], callback_data=f'{ACCOUNT_IND}{SP}{button}')
             for button, text in ACCOUNT_KB.items()])

    try:
        bot.delete_message(message.chat.id, user.last_message())
    except Exception:
        pass

    lm = bot.send_message(message.chat.id, ACCOUNT_TEXT[user.lang], reply_markup=kb)
    user.last_message(lm.message_id)


@bot.callback_query_handler(func=lambda call: (call.data.split(SP)[0] == ACCOUNT_IND and
                                               call.data.split(SP)[1] == 'status'))
def show_status(call):

    user = Users.get_user(user_id=str(call.message.chat.id))

    kb = InlineKeyboardMarkup(row_width=1)

    if BACK_IND in call.data.split(SP):
        kb.add(*[InlineKeyboardButton(text=text[user.lang], callback_data=f'{ACCOUNT_IND}{SP}{button}')
                 for button, text in ACCOUNT_KB.items()])

        bot.edit_message_text(ACCOUNT_TEXT[user.lang], call.message.chat.id, call.message.message_id, reply_markup=kb)
    else:
        if user.current_payment.type == 'expired':
            status = STATUS_TEXT['expired'][user.lang]
        elif user.current_payment.type == 'trial':
            status = STATUS_TEXT['trial'][user.lang] + user.current_payment.end_date.strftime("%d.%m.%Y")
        elif user.current_payment.type == 'paid':
            status = STATUS_TEXT['paid'][user.lang] + user.current_payment.end_date.strftime("%d.%m.%Y")

        kb.add(InlineKeyboardButton(text=BACK_BUTTON[user.lang],
                                    callback_data=f'{ACCOUNT_IND}{SP}{STATUS_IND}{SP}{BACK_IND}'))
        bot.edit_message_text(status, call.message.chat.id, call.message.message_id, reply_markup=kb)


@bot.callback_query_handler(func=lambda call: (call.data.split(SP)[0] == ACCOUNT_IND and
                                               call.data.split(SP)[1] == PAYMENT_IND))
def show_payment(call):

    user = Users.get_user(user_id=str(call.message.chat.id))

    kb = InlineKeyboardMarkup(row_width=1)
    step = call.data.split(SP)[-1]

    if step == BACK_IND:
        data = call.data.split(SP)[0:-2]
        ind = '-'.join(data)

        if data[-1] == 'account':
            act_text = ACCOUNT_TEXT
            act_kb = ACCOUNT_KB
            has_prev_menu = False
        elif data[-1] == 'payment':
            act_text = PAYMENT_CURRENCY_TEXT
            act_kb = PAYMENT_CURRENCY_KB
            has_prev_menu = True
        elif data[-1] in PAYMENT_CURRENCY_KB.keys():
            act_text = PAYMENT_TEXT
            act_kb = PAYMENT_OPTIONS_KB
            has_prev_menu = True
        elif data[-1] == 'signals':
            act_text = PAYMENT_TEXT
            act_kb = copy.deepcopy(SIGNALS_PACKAGES_KB)
            currency = data[2]
            for button, txt in act_kb.items():
                price = f_price(PACKAGES[button]["price"] / RATES[currency])
                act_kb[button][user.lang] = \
                    txt[user.lang] + f'{price} {currency}'
            has_prev_menu = True
        elif data[-1] == 'following':
            act_text = PAYMENT_TEXT
            act_kb = copy.deepcopy(FOLLOWING_PACKAGES_KB)
            currency = data[2]
            for button, txt in act_kb.items():
                if button in FOLLOWING_PACKAGES.keys():
                    price = f_price(FOLLOWING_PACKAGES[button]["price"] / RATES[currency])
                    act_kb[button][user.lang] = \
                        txt[user.lang] + f'{price} {currency}'
                else:
                    act_kb[button][user.lang] = txt[user.lang]
            has_prev_menu = True

        kb.add(*[InlineKeyboardButton(text=text[user.lang], callback_data=f'{ind}{SP}{button}')
                 for button, text in act_kb.items()])

        if has_prev_menu:
            kb.add(InlineKeyboardButton(text=BACK_BUTTON[user.lang],
                                        callback_data=f'{ind}{SP}{BACK_IND}'))

        bot.edit_message_text(act_text[user.lang], call.message.chat.id, call.message.message_id, reply_markup=kb)

    elif step == PAYMENT_IND:
        ind = call.data
        text = PAYMENT_CURRENCY_TEXT[user.lang]

        for button, txt in PAYMENT_CURRENCY_KB.items():
            kb.add(InlineKeyboardButton(
                   text=txt[user.lang],
                   callback_data=f'{ind}{SP}{button}'))
        kb.add(InlineKeyboardButton(text=BACK_BUTTON[user.lang],
                                    callback_data=f'{ind}{SP}{BACK_IND}'))

        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=kb)

    elif step in PAYMENT_CURRENCY_KB.keys():
        ind = call.data
        text = PAYMENT_TEXT[user.lang]

        for button, txt in PAYMENT_OPTIONS_KB.items():
            b_txt = txt[user.lang]
            kb.add(InlineKeyboardButton(text=b_txt,
                                        callback_data=f'{ind}{SP}{button}'))
        kb.add(InlineKeyboardButton(text=BACK_BUTTON[user.lang],
                                    callback_data=f'{ind}{SP}{BACK_IND}'))

        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=kb)

    elif step in PAYMENT_OPTIONS_KB.keys():
        if step == 'signals':
            ind = call.data
            currency = call.data.split(SP)[2]
            text = PAYMENT_TEXT[user.lang]

            for button, txt in SIGNALS_PACKAGES_KB.items():
                price = f_price(PACKAGES[button]["price"] / RATES[currency])
                b_txt = txt[user.lang] + f'{price} {currency}'
                kb.add(InlineKeyboardButton(text=b_txt,
                                            callback_data=f'{ind}{SP}{button}'))
            kb.add(InlineKeyboardButton(text=BACK_BUTTON[user.lang],
                                        callback_data=f'{ind}{SP}{BACK_IND}'))

            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=kb)
        elif step == 'following':
            ind = call.data
            currency = call.data.split(SP)[2]
            text = PAYMENT_TEXT[user.lang]

            for button, txt in FOLLOWING_PACKAGES_KB.items():
                if button in FOLLOWING_PACKAGES.keys():
                    price = f_price(FOLLOWING_PACKAGES[button]["price"] / RATES[currency])
                    b_txt = txt[user.lang] + f'{price} {currency}'
                else:
                    b_txt = txt[user.lang]
                kb.add(InlineKeyboardButton(text=b_txt,
                                            callback_data=f'{ind}{SP}{button}'))
            kb.add(InlineKeyboardButton(text=BACK_BUTTON[user.lang],
                                        callback_data=f'{ind}{SP}{BACK_IND}'))

            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=kb)

    elif step in SIGNALS_PACKAGES_KB.keys():
        ind = call.data
        currency = call.data.split(SP)[2]
        price = f_price(PACKAGES[step]['price']/RATES[currency])
        text = CHECKOUT_TEXT[user.lang] + WALLETS[currency] + f'\n{price} {currency}'

        for button, txt in CHECKOUT_KB.items():
            kb.add(InlineKeyboardButton(text=txt[user.lang],
                                        callback_data=f'{ind}{SP}{button}'))
        kb.add(InlineKeyboardButton(text=BACK_BUTTON[user.lang],
                                    callback_data=f'{ind}{SP}{BACK_IND}'))

        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=kb)

    elif step in FOLLOWING_PACKAGES_KB.keys():
        ind = call.data
        currency = call.data.split(SP)[2]

        if step != 'fp_4':
            price = f_price(FOLLOWING_PACKAGES[step]['price'] / RATES[currency])
            text = CHECKOUT_TEXT[user.lang] + WALLETS[currency] + f'\n{price} {currency}'

            for button, txt in CHECKOUT_KB.items():
                kb.add(InlineKeyboardButton(text=txt[user.lang],
                                            callback_data=f'{ind}{SP}{button}'))
            kb.add(InlineKeyboardButton(text=BACK_BUTTON[user.lang],
                                        callback_data=f'{ind}{SP}{BACK_IND}'))

            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=kb)
        elif step == 'fp_4':
            text = VIP_FOLLOWING_TEXT[user.lang]
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id)

    elif step == 'paid':

        ind = call.data
        package = ind.split(SP)[-2]

        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=False)
        bot.send_message(call.message.chat.id, f'{TXID_REQUEST[user.lang]}')

        if package in SIGNALS_PACKAGES_KB.keys():
            amount = PACKAGES[package]['price']
            duration = PACKAGES[package]['duration']
            payment_type = 'paid'
        elif package in FOLLOWING_PACKAGES_KB.keys():
            amount = FOLLOWING_PACKAGES[package]['price']
            duration = FOLLOWING_PACKAGES[package]['duration']
            payment_type = 'following'

        PrePayments.create(user_id=str(call.message.chat.id),
                           payment_type=payment_type,
                           amount=amount,
                           duration=duration)


@bot.callback_query_handler(func=lambda call: (call.data.split(SP)[0] == ACCOUNT_IND and
                                               call.data.split(SP)[1] == REFERRALS_IND))
def show_referrals(call):

    user = Users.get_user(user_id=str(call.message.chat.id))

    kb = InlineKeyboardMarkup(row_width=1)

    if BACK_IND in call.data.split(SP):
        kb.add(*[InlineKeyboardButton(text=text[user.lang], callback_data=f'{ACCOUNT_IND}{SP}{button}')
                 for button, text in ACCOUNT_KB.items()])
        bot.edit_message_text(ACCOUNT_TEXT[user.lang], call.message.chat.id, call.message.message_id, reply_markup=kb)
    else:
        status = user.ref_status

        kb.add(InlineKeyboardButton(text=BACK_BUTTON[user.lang],
                                    callback_data=f'{ACCOUNT_IND}{SP}{REFERRALS_IND}{SP}{BACK_IND}'))
        bot.edit_message_text(status, call.message.chat.id, call.message.message_id, reply_markup=kb)


"""
SIGNALS
"""


@bot.message_handler(content_types='text', func=lambda message: message.text.split()[-1] in START_KB['signals'].values())
def show_signals(message):

    user = Users.get_user(user_id=str(message.chat.id))

    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(*[InlineKeyboardButton(text=SIGNALS_KB_PICS[button] + text[user.lang], callback_data=f'{SIGNALS_IND}{SP}{button}')
             for button, text in SIGNALS_KB.items()])

    try:
        bot.delete_message(message.chat.id, user.last_message())
    except Exception:
        pass

    lm = bot.send_message(message.chat.id, SIGNALS_TEXT[user.lang], reply_markup=kb)
    user.last_message(lm.message_id)


@bot.callback_query_handler(func=lambda call: (call.data.split(SP)[0] == SIGNALS_IND and
                                               call.data.split(SP)[1] == EXCHANGES_IND))
def show_exchanges(call):

    user = Users.get_user(user_id=str(call.message.chat.id))
    text = EXCHANGES_TEXT[user.lang]
    kb = InlineKeyboardMarkup(row_width=1)

    if BACK_IND in call.data.split(SP):

        kb.add(*[InlineKeyboardButton(text=text[user.lang], callback_data=f'{SIGNALS_IND}{SP}{button}')
                 for button, text in SIGNALS_KB.items()])
        bot.edit_message_text(SIGNALS_TEXT[user.lang], call.message.chat.id, call.message.message_id, reply_markup=kb)

    else:

        if call.data.split(SP)[-1] in EXCHANGES_KB.keys():
            user.upd_exchanges(call.data.split(SP)[-1])

        for button, txt in EXCHANGES_KB.items():
            if button in user.active_exchanges:
                b_text = C_B_BUTTONS['checked'] + txt
            else:
                b_text = C_B_BUTTONS['unchecked'] + txt

            kb.add(InlineKeyboardButton(text=b_text,
                                        callback_data=f'{SIGNALS_IND}{SP}{EXCHANGES_IND}{SP}{button}'))
        kb.add(InlineKeyboardButton(text=BACK_BUTTON[user.lang],
                                    callback_data=f'{SIGNALS_IND}{SP}{EXCHANGES_IND}{SP}{BACK_IND}'))
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=kb)


@bot.callback_query_handler(func=lambda call: (call.data.split(SP)[0] == SIGNALS_IND and
                                               call.data.split(SP)[1] == STRATEGIES_IND))
def show_strategies(call):

    user = Users.get_user(user_id=str(call.message.chat.id))
    text = STRATEGIES_TEXT[user.lang]
    kb = InlineKeyboardMarkup(row_width=1)

    if BACK_IND in call.data.split(SP):

        kb.add(*[InlineKeyboardButton(text=text[user.lang], callback_data=f'{SIGNALS_IND}{SP}{button}')
                 for button, text in SIGNALS_KB.items()])
        bot.edit_message_text(SIGNALS_TEXT[user.lang], call.message.chat.id, call.message.message_id, reply_markup=kb)
    else:

        if call.data.split(SP)[-1] in STRATEGIES_KB.keys():
            user.upd_strategies(call.data.split(SP)[-1])

        for button, txt in STRATEGIES_KB.items():
            if button in user.active_strategies:
                b_text = C_B_BUTTONS['checked'] + txt
            else:
                b_text = C_B_BUTTONS['unchecked'] + txt

            kb.add(InlineKeyboardButton(text=b_text,
                                        callback_data=f'{SIGNALS_IND}{SP}{STRATEGIES_IND}{SP}{button}'))
        kb.add(InlineKeyboardButton(text=BACK_BUTTON[user.lang],
                                    callback_data=f'{SIGNALS_IND}{SP}{STRATEGIES_IND}{SP}{BACK_IND}'))
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=kb)


@bot.callback_query_handler(func=lambda call: (call.data.split(SP)[0] == SIGNALS_IND and
                                               call.data.split(SP)[1] == 'currencies'))
def show_currencies(call):

    user = Users.get_user(user_id=str(call.message.chat.id))
    text = CURRENCIES_TEXT[user.lang]
    kb = InlineKeyboardMarkup(row_width=1)

    if BACK_IND in call.data.split(SP):

        kb.add(*[InlineKeyboardButton(text=text[user.lang], callback_data=f'{SIGNALS_IND}{SP}{button}')
                 for button, text in SIGNALS_KB.items()])
        bot.edit_message_text(SIGNALS_TEXT[user.lang], call.message.chat.id, call.message.message_id, reply_markup=kb)
    else:

        if call.data.split(SP)[-1] in CURRENCIES_KB.keys():
            user.upd_currencies(call.data.split(SP)[-1])

        for button, txt in CURRENCIES_KB.items():
            if button in user.active_currencies:
                b_text = C_B_BUTTONS['checked'] + txt
            else:
                b_text = C_B_BUTTONS['unchecked'] + txt

            kb.add(InlineKeyboardButton(text=b_text,
                                        callback_data=f'{SIGNALS_IND}{SP}{CURRENCIES_IND}{SP}{button}'))
        kb.add(InlineKeyboardButton(text=BACK_BUTTON[user.lang],
                                    callback_data=f'{SIGNALS_IND}{SP}{CURRENCIES_IND}{SP}{BACK_IND}'))
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=kb)


@bot.message_handler(content_types='text', func=lambda message: message.text.split()[-1] in START_KB['statistics'].values())
def show_statistics(message):

    user = Users.get_user(user_id=str(message.chat.id))
    text = STATISTICS_TEXT[user.lang]

    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(*[InlineKeyboardButton(text=text, callback_data=f'{STATISTICS_IND}{SP}{button}')
             for button, text in STRATEGIES_KB.items()])

    try:
        bot.delete_message(message.chat.id, user.last_message())
    except Exception:
        pass

    lm = bot.send_message(message.chat.id, text, reply_markup=kb)
    user.last_message(lm.message_id)


@bot.callback_query_handler(func=lambda call: (call.data.split(SP)[0] == STATISTICS_IND))
def show_strategies(call):

    user = Users.get_user(user_id=str(call.message.chat.id))
    strategy = call.data.split(SP)[-1]

    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception:
        pass

    if strategy == '1':
        with open('AI_Trade_stat_with_leverage.jpg', 'rb') as file:
            pic = file.read()
            bot.send_photo(chat_id=user.chat_id, photo=pic)
            time.sleep(0.5)
        with open('AI_Trade_stat_wo_leverage.jpg', 'rb') as file:
            pic = file.read()
            bot.send_photo(chat_id=user.chat_id, photo=pic)
    elif strategy == '2':
        with open('WBCC_Trend_stat_with_leverage.jpg', 'rb') as file:
            pic = file.read()
            bot.send_photo(chat_id=user.chat_id, photo=pic)
            time.sleep(0.5)
        with open('WBCC_Trend_stat_wo_leverage.jpg', 'rb') as file:
            pic = file.read()
            bot.send_photo(chat_id=user.chat_id, photo=pic)


@bot.message_handler(content_types='text', func=lambda message: message.text.split()[-1] in START_KB['following'].values())
def show_following(message):

    user = Users.get_user(user_id=str(message.chat.id))
    text = FOLLOWING_TEXT[user.lang]

    try:
        bot.delete_message(message.chat.id, user.last_message())
    except Exception:
        pass

    lm = bot.send_message(message.chat.id, text=text)
    user.last_message(lm.message_id)


@bot.message_handler(content_types='text', func=lambda message: message.text.split()[-1] in START_KB['help'].values())
def show_help(message):

    user = Users.get_user(user_id=str(message.chat.id))
    text = HELP_TEXT[user.lang]

    try:
        bot.delete_message(message.chat.id, user.last_message())
    except Exception:
        pass

    lm = bot.send_message(message.chat.id, text=text)
    user.last_message(lm.message_id)


@bot.message_handler(func=lambda message: PrePayments.has_prepayment(str(message.chat.id)))
def checkout(message):
    user = Users.get_user(user_id=str(message.chat.id))
    txid = message.text
    if txid in ABORT_BUTTON.values():
        kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        kb.add(*[KeyboardButton(text=START_KB_PICS[button] + ' ' + START_KB[button][user.lang])
                 for button in START_KB.keys()])
        bot.send_message(message.chat.id, HELP_TEXT[user.lang], reply_markup=kb)
        PrePayments.cancel(str(message.chat.id))
        return
    elif (len(txid) == 64 and txid.isalnum()) or (len(txid) == 11 and txid.isdigit()):
        user_id, payment_type, amount, duration = PrePayments.read(user.chat_id)

        Payments.create(user_id=user_id,
                        payment_type=payment_type,
                        payment_end_date=datetime.datetime.now() + datetime.timedelta(days=duration * 30),
                        amount=amount,
                        tx_id=txid)
        PrePayments.cancel(str(message.chat.id))

        kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        kb.add(*[KeyboardButton(text=START_KB_PICS[button] + ' ' + START_KB[button][user.lang])
                 for button in START_KB.keys()])
        bot.send_message(message.chat.id, PAID_TEXT[user.lang], reply_markup=kb)
    else:
        kb = ReplyKeyboardMarkup(resize_keyboard=True)
        kb.add(KeyboardButton(ABORT_BUTTON[user.lang]))
        bot.send_message(message.chat.id, INVALID_TXID[user.lang] + ABORT_BUTTON[user.lang],
                         reply_markup=kb)


def send_signal(signal_path, exchange, strategy, pair):

    receivers = Users.get_receivers(exchange, strategy, pair)
    users = Users.read()

    with open(signal_path, 'rb') as file:
        for user in receivers:
            pic = file.read()
            payment = user.active_payment()
            if payment.is_valid:
                bot.send_photo(chat_id=user.chat_id, photo=pic)
                time.sleep(0.5)
            file.seek(0)

    for user in users:
        payment = user.active_payment()
        if payment.payment_end_date < datetime.datetime.now():
            bot.send_message(user.chat_id, SUBSCRIPTION_EXPIRED[user.lang])
            time.sleep(0.5)


def send_notification(text, chat_id=None):
    log = []

    if chat_id:
        try:
            bot.send_message(chat_id, text)
            log.append(f'{chat_id} - OK')
        except Exception as e:
            log.append(f'{chat_id} - {e}')
            pass
    else:
        users = Users.read()
        for user in users:
            try:
                bot.send_message(user.chat_id, text)
                log.append(f'{user.chat_id} - OK')
                time.sleep(0.5)
            except Exception as e:
                log.append(f'{user.chat_id}, - {e}') 
                continue
    with open('notification_log.txt', 'w') as file:
        file.write('\n'.join(log))


def start_bot():
    bot.polling()


start_bot()
