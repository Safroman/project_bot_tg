from main import start_bot, bot, send_signal, send_notification
from config import WEBHOOK_PATH, SIGNALS_PATH, NOTIFICATION_PATH, STATUS_PATH, WEBHOOK_URL, CERT_NAME
from flask import Flask, request, abort
from telebot.types import Update
import time
from threading import Thread


version = 'production'
# version = 'develop'


app = Flask(__name__)

if version == 'production':

    @app.route(WEBHOOK_PATH, methods=['POST'])
    def webhook():
        if request.headers.get('content-type') == 'application/json':
            json_string = request.get_data().decode('utf-8')
            update = Update.de_json(json_string)
            bot.process_new_updates([update])
            return ''
        else:
            abort(403)


    @app.route(SIGNALS_PATH, methods=['POST'])
    def sending_signals():
        signal_path = request.form['signal_path']
        exchange = request.form['exchange']
        strategy = request.form['strategy']
        pair = request.form['pair']
        log = open('signals_log.txt', 'w')
        log.write(signal_path)
        log.close()
        # s_sending = Thread(target=send_signal, args=(signal_path, exchange, strategy, pair))
        # s_sending.start()
        return ''


    @app.route(NOTIFICATION_PATH, methods=['POST'])
    def sending_notification():
        chat_id = request.form['chat_id']
        text = request.form['text']
        log = open('notification_log.txt', 'w')
        log.write(text)
        log.close()
        # n_sending = Thread(target=send_notification, args=(text, chat_id))
        # n_sending.start()
        return ''

    @app.route(STATUS_PATH, methods=['GET'])
    def chk_status():
        return 'OK'


    bot.remove_webhook()
    time.sleep(1)

    bot.set_webhook((WEBHOOK_URL + WEBHOOK_PATH),
                    certificate=open(CERT_NAME, 'r'))

else:
    bot.remove_webhook()
    time.sleep(1)
    start_bot()
