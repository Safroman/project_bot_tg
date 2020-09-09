from main import start_bot, bot, send_signal
from config import WEBHOOK_PATH, WEBHOOK_URL, SIGNALS_PATH, CERT_NAME
from flask import Flask, request, abort
from telebot.types import Update
import time


# version = 'production'
version = 'develop'


app = Flask(__name__)


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


if __name__ == '__main__':

    if version == 'production':

        bot.remove_webhook()
        time.sleep(1)

        bot.set_webhook((WEBHOOK_URL + WEBHOOK_PATH),
                        certificate=open(CERT_NAME, 'r'))
        app.run(debug=True)

    else:
        bot.remove_webhook()
        time.sleep(1)
        start_bot()

