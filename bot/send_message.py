import requests
import mongoengine as me


me.connect('AlgTrdSignals_bot', host='mongodb://algtrd:sieNg4ta@db.algtrd.com:27017/?compressors=zlib&ssl=true',
           authentication_source='admin')


class Users(me.Document):

    user_id = me.StringField()
    user_name = me.StringField()
    language = me.StringField()
    reg_date = me.DateTimeField()
    current_payment = me.ReferenceField('Payments')
    exchanges = me.ListField()
    strategies = me.ListField()
    currencies = me.ListField()
    ref_link = me.StringField()
    referrals = me.ListField()
    last_message_id = me.StringField()
    txid_requested = me.IntField()

    @classmethod
    def read(cls, user_id=None):
        if user_id:
            return cls.objects.get(user_id=user_id)
        else:
            return cls.objects()


class Payments(me.Document):
    user_id = me.StringField()
    payment_type = me.StringField()
    payment_date = me.DateTimeField()
    payment_end_date = me.DateTimeField()
    amount = me.FloatField()
    tx_id = me.StringField()
    confirmed = me.IntField()


GLOBAL_IP = 'https://sys.algtrd.com'
PATH = '/initiator/send_notification'


"""
chat_id takes empty or one chat_it argument' 
"""

text = 'Уважаемые пользователи. В случае вопросов обращайтесь в @AlgTrd_Sup'

users = Users.read()

for user in users:
    params = {'chat_id': str(user.user_id),
              'text': text}
    r = requests.post((GLOBAL_IP + PATH), data=params)
    print(user.user_id, r)

