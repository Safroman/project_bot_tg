import requests
from main import send_signal

#
# def index():
#     params = {'signal_path': 'test_path',
#               'exchange': 'test_exchange',
#               'strategy': 'test_strategy',
#               'pair': 'test_pair'}
#     requests.post('https://sys.algtrd.com/initiator/send_signal', data=params)

def index():
    send_signal()

index()