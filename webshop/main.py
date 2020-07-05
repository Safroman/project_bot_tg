from webshop.bot.main import start_bot, bot
from webshop.bot import config
from flask import Flask, request, abort
from telebot.types import Update
from api.api_main import api_app
import time


app = Flask(__name__)


@app.route(config.WEBHOOK_PATH, methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        abort(403)


if __name__ == '__main__':
    api_app.run(debug=True)
    start_bot()
    bot.polling()

    bot.remove_webhook()
    time.sleep(1)

    bot.set_webhook(config.WEBHOOK_URL,
                    certificate=open('webhook_cert.pem', 'r')
                   )

    app.run(debug=True)
