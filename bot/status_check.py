from telebot import TeleBot
from flask import Flask, request, abort
import requests
import time


TOKEN = ''
USER_LIST = ['', '']


bot = TeleBot(TOKEN)
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


if __name__ == '__main__':

    bot.remove_webhook()
    time.sleep(1)

    bot.set_webhook(WEBHOOK_URL,
                    certificate=open(CERT_NAME, 'r'))
    app.run(debug=True)
else:

    app.run()
    # bot.polling()
    while True:
        try:
            requests.get('http://127.0.0.1:5000/AlgTrdSignals_bot/send_signal')
        except requests.exceptions.RequestException:
            for user in USER_LIST:
                bot.send_message(user, 'SOS')
        time.sleep(60)
