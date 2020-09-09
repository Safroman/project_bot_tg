import requests

GLOBAL_IP = 'https://sys.algtrd.com:5000'
LOCAL_IP = '127.0.0.1:5000'
PATH = '/test'

pic_folder = 'some_folder'
pic_name = 'some_name'
exchange = 'test_exc'
strategy = 'test_strat'
pair = 'test_pair'


params = {'signal_path': (pic_folder + pic_name),
          'exchange': exchange,
          'strategy': strategy,
          'pair': pair}

requests.post((GLOBAL_IP + PATH), data=params)
