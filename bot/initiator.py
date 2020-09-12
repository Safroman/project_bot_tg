from main import start_bot, bot, send_signal, send_notification
from config import WEBHOOK_PATH, SIGNALS_PATH, STATUS_PATH, NOTIFICATION_PATH, WEBHOOK_URL, CERT_NAME
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
        send_signal(signal_path, exchange, strategy, pair)
        return ''


    @app.route(NOTIFICATION_PATH, methods=['POST'])
    def sending_notification():
        chat_id = request.form['chat_id']
        text = request.form['text']
        n_sending = Thread(target=send_notification, args=(text, chat_id))
        n_sending.start()
        # send_notification(text, chat_id)

        return ''


    bot.remove_webhook()
    time.sleep(1)

    bot.set_webhook(WEBHOOK_URL,
                    certificate=open('webhook_cert.pem', 'r'))

else:
    bot.remove_webhook()
    time.sleep(1)
    start_bot()
