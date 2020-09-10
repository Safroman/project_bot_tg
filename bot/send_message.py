import requests

# GLOBAL_IP = 'https://sys.algtrd.com'

PATH = '/initiator/send_notification'

"""
chat_id takes empty or one chat_it argument' 
"""

params = {'chat_id': '390188983',
          'text': 'Владимир, Ваш бот работает - профита Вам!'}


r = requests.post((GLOBAL_IP + PATH), data=params)
print(r)
