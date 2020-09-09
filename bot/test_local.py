import requests

GLOBAL_IP = 'http://34.78.227.221'

# GLOBAL_IP = 'https://sys.algtrd.com'
PATH = '/initiator/send_signal'

pic_folder = 'some_folder'
pic_name = 'some_name'
exchange = 'test_exc'
strategy = 'test_strat'
pair = 'test_pair'


params = {'signal_path': (pic_folder + pic_name),
          'exchange': exchange,
          'strategy': strategy,
          'pair': pair}


chat_id = ['390188983', '886841530']
text = ''


# params = {'chat_id': '390188983',
#           'text': 'some another text'}
r = requests.post((GLOBAL_IP + PATH), data=params)
print(r)
