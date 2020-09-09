import mongoengine as me
import datetime
# from config import DB_NAME, HOST_NAME, BOT_NAME
from config import DB_NAME, BOT_NAME
from contents import *

# me.connect(DB_NAME, host='mongodb://algtrd:sieNg4ta@db.algtrd.com:27017/?compressors=zlib&ssl=true',
#            authentication_source='admin')

me.connect(DB_NAME)


class Users(me.Document):

    user_id = me.StringField()
    user_name = me.StringField(default='none')
    language = me.StringField()
    reg_date = me.DateTimeField(default=datetime.datetime.now())
    current_payment = me.ReferenceField('Payments')
    exchanges = me.ListField(me.StringField(), default=[num for num in EXCHANGES_KB.keys()])
    strategies = me.ListField(me.StringField(), default=[num for num in STRATEGIES_KB.keys()])
    currencies = me.ListField(me.StringField(), default=[num for num in CURRENCIES_KB.keys()])
    ref_link = me.StringField(default='none')
    referrals = me.ListField(me.ReferenceField('self'))
    last_message_id = me.StringField()
    txid_requested = me.IntField(default=0)

    @classmethod
    def create(cls, **kwargs):
        user = cls.objects.create(**kwargs)
        return user

    @classmethod
    def read(cls, user_id=None):
        if user_id:
            return cls.objects.get(user_id=user_id)
        else:
            return cls.objects()

    @classmethod
    def get_user(cls, user_id):
        user = cls.objects.get(user_id=user_id)
        payment = user.active_payment()
        if datetime.datetime.now() >= payment.payment_end_date:
            Payments.update(payment.id, payment_type='expired')
        return user

    @property
    def lang(self):
        return self.language

    def set_language(self, lang):
        self.language = lang
        self.save()

    def last_message(self, m_id=''):
        if m_id:
            self.last_message_id = str(m_id)
            self.save()
        else:
            return self.last_message_id

    def gen_ref_link(self):
        link = f'https://telegram.me/{BOT_NAME}?start={self.id}'
        self.ref_link = link
        self.save()

    def add_referral(self, ref):
        referrals = self.referrals
        referrals.append(ref)
        self.referrals = referrals
        self.save()

    @property
    def active_exchanges(self):
        return self.exchanges

    def upd_exchanges(self, choice):
        new_exchanges = self.exchanges
        if choice in self.exchanges:
            new_exchanges.remove(choice)
        else:
            new_exchanges.append(choice)
        if len(new_exchanges) == 0:
            if choice != '1':
                new_exchanges.append('1')
            else:
                new_exchanges.append('2')
        self.exchanges = new_exchanges
        self.save()

    @property
    def active_strategies(self):
        return self.strategies

    def upd_strategies(self, choice):
        new_strategies = self.strategies
        if choice in self.strategies:
            new_strategies.remove(choice)
        else:
            new_strategies.append(choice)
        if len(new_strategies) == 0:
            if choice != '1':
                new_strategies.append('1')
            else:
                new_strategies.append('2')
        self.strategies = new_strategies
        self.save()

    @property
    def active_currencies(self):
        return self.currencies

    def upd_currencies(self, choice):
        new_currencies = self.currencies
        if choice in self.currencies:
            new_currencies.remove(choice)
        else:
            new_currencies.append(choice)
        if len(new_currencies) == 0:
            if choice != '1':
                new_currencies.append('1')
            else:
                new_currencies.append('2')
        self.currencies = new_currencies
        self.save()

    @property
    def ref_status(self):
        text = REFERRALS_TEXT_l1[self.lang] + '\n' + \
               self.ref_link + '\n' + \
               REFERRALS_TEXT_l2[self.lang] + str(len(self.referrals))
        return text

    def active_payment(self):
        payments = Payments.objects.filter(user_id=self.user_id, confirmed=1, payment_type__ne='following')
        active_payment = payments.order_by('-payment_end_date')
        if len(active_payment) != 0:
            self.current_payment = active_payment[0]
            self.save()
        return self.current_payment

    @classmethod
    def get_receivers(cls, exchange, strategy, pair):

        for key, value in EXCHANGES_KB.items():
            if value == exchange:
                exc_code = key
        for key, value in STRATEGIES_KB.items():
            if value == strategy:
                strat_code = key
        for key, value in CURRENCIES_KB.items():
            if value == pair:
                cur_code = key

        return cls.objects.filter(exchanges=exc_code, strategies=strat_code, currencies=cur_code)

    @property
    def chat_id(self):
        return self.user_id


class Payments(me.Document):

    user_id = me.StringField()
    payment_type = me.StringField()
    payment_date = me.DateTimeField(default=datetime.datetime.now())
    payment_end_date = me.DateTimeField(default=(datetime.datetime.now()+datetime.timedelta(days=7)))
    amount = me.FloatField(default=0)
    tx_id = me.StringField(default='none')
    confirmed = me.IntField(default=0)

    @classmethod
    def create(cls, **kwargs):
        payment = cls.objects.create(**kwargs)
        return payment

    @classmethod
    def read(cls):
        pass

    @classmethod
    def update(cls, payment_id, **kwargs):
        payment = cls.objects.get(id=payment_id)
        if 'payment_type' in kwargs.keys():
            payment.payment_type = kwargs['payment_type']
        if 'confirmed' in kwargs.keys():
            payment.confirmed = kwargs['confirmed']
        payment.save()

    @property
    def is_valid(self):
        if self.payment_end_date >= datetime.datetime.now():
            return self.confirmed
        else:
            return False

    @property
    def type(self):
        return self.payment_type

    @property
    def end_date(self):
        return self.payment_end_date


class PrePayments(me.Document):

    user_id = me.StringField()
    payment_type = me.StringField()
    amount = me.FloatField(default=0)
    duration = me.IntField()

    @classmethod
    def create(cls, user_id, payment_type, amount, duration):
        prepayments = cls.objects.filter(user_id=user_id)
        for payment in prepayments:
            payment.delete()
        cls.objects.create(user_id=user_id,
                           payment_type=payment_type,
                           amount=amount,
                           duration=duration)
        return

    @classmethod
    def read(cls, user_id):
        prepayment = cls.objects.filter(user_id=user_id)[0]
        return prepayment.user_id, prepayment.payment_type, prepayment.amount, prepayment.duration

    @classmethod
    def cancel(cls, user_id):
        prepayments = cls.objects.filter(user_id=user_id)
        for payment in prepayments:
            payment.delete()

    @classmethod
    def has_prepayment(cls, user_id):
        if len(cls.objects.filter(user_id=user_id)) > 0:
            return True
        else:
            return False
