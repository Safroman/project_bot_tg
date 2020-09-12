import requests

GLOBAL_IP = 'http://34.78.227.221'
# GLOBAL_IP = 'https://sys.algtrd.com'

# PATH = '/initiator/send_signal'
PATH = '/initiator/send_notification'

pic_folder = ''
pic_name = 'AI_Trade_stat_with_leverage.jpg'
exchange = 'Binance'
strategy = 'Trend_4h'
pair = 'XBT'


# params = {'signal_path': (pic_folder + pic_name),
#           'exchange': exchange,
#           'strategy': strategy,
#           'pair': pair}

params = {'chat_id': '390188',
          'text': 'Сигнал Тестовый - простите за беспокойство!'}

chat_id = ['390188983', '886841530']


r = requests.post((GLOBAL_IP + PATH), data=params)
print(r)
