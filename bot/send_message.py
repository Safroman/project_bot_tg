import requests

GLOBAL_IP = 'https://sys.algtrd.com'

PATH = '/initiator/send_notification'

"""
chat_id takes empty or one chat_it argument' 
"""

params = {'chat_id': '390188983',
          'text': 'Добрый день, мы рады всех приветствовать в нашей системе! '
                  'У всех новых клиентов есть тестовый период для проверки наших сигналов, '
                  'пожалуйста напишите сообщение - буду тестировать- вот сюда @AlgTrd_support '
                  'что бы Вам начали приходить сигналы. Спасибо и профита Вам!'
                  '\n\nЕсли Вы уже писали в @AlgTrd_support, повторно писать не нужно.'}


r = requests.post((GLOBAL_IP + PATH), data=params)
print(r)
