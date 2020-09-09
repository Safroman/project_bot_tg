import requests

GLOBAL_IP = '34.78.227.221'
LOCAL_IP = '127.0.0.1:5000'
PATH = 'initiator/send_notification'

pic_folder = 'some_folder'
pic_name = 'some_name'
exchange = 'test_exc'
strategy = 'test_strat'
pair = 'test_pair'


# params = {'signal_path': (pic_folder + pic_name),
#           'exchange': exchange,
#           'strategy': strategy,
#           'pair': pair}

params = {'text': 'some_text'}

requests.post((GLOBAL_IP + PATH), data=params)
