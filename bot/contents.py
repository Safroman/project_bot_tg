
LANGUAGE_KB = {'RU': u'\U0001F1F7\U0001F1FA Русский',
               'EN': u'\U0001F1FA\U0001F1F8 English'}

GREETINGS = {'RU': "\U00002757 \U00002668 *Добро пожаловать в AlgTrd* \U00002668 \U00002757"
                   "\n\n"
                   "Совместно с нашими партнерами, была разработана удобная "
                   "система для авто торговли на биржах Bitmex и Binance по двум "
                   "алгортимам: *Trend* и *Scalp*."
                   "\n\n"
                   "На примере торгов на парах BTCUSDTPERP или XBTUSD:"
                   "\n\n"
                   "\U0001F4C8 Средняя доходность в месяц с 3 плечом составляет от *15 до 30%.*"
                   "\n\n"
                   "С 1 января по 1 сентября 2020 года по расчету статистики - "
                   "доходность по каждому алгоритму составила *400+%*"
                   "\n\n"
                   "\U0001F4B8 Стоимость подключения к одному алгоритму, и зависимость от Вашего депозита:"
                   "\n\n"
                   "Тест на 1 месяц (если нужен):  500-999$ - 50 USDT \n"
                   "1. 1000-2499$ - 125 USDT\n"
                   "2. 2500-4999$ - 250 USDT\n"
                   "3. 5000 и выше - 2.5% от депозита.\n"
                   "\n\n"
                   "*Подробнее о том как подключиться:* https://telegra.ph/Sistema-avto-torgovli-AlgTrd-09-04"
                   "\n\n"
                   "\U000027A1 Контакт для вопросов: [@AlgTrd_support](URL)",
             'EN': "\U00002757 \U00002668 *Welcome to AlgTrd* \U00002668 \U00002757"
                   "\n\n"
                   "Together with our partners, a convenient system for auto trading on the Bitmex and Binance "
                   "exchanges was developed using two algorithms: *Trend* и *Scalp*."
                   "\n\n"
                   "Using the example of trading on BTCUSDTPERP or XBTUSD pairs:"
                   "\n\n"
                   "\U0001F4C8 Average monthly profitability with 3 leverage is from *15 to 30%.*"
                   "\n\n"
                   "From January 1 to September 1, 2020, according to the calculation of statistics, "
                   "the profitability of each algorithm is *400+%*"
                   "\n\n"
                   "\U0001F4B8 The cost of connecting to one algorithm, and dependence on your deposit:"
                   "\n\n"
                   "Test for 1 month (if needed):  500-999$ - 50 USDT \n"
                   "1. 1000-2499$ - 125 USDT\n"
                   "2. 2500-4999$ - 250 USDT\n"
                   "3. 5000 and more - 2.5% of deposit.\n"
                   "\n\n"
                   "*More details on how to connect:* https://telegra.ph/Sistema-avto-torgovli-AlgTrd-09-04"
                   "\n\n"
                   "\U000027A1 Contact for questions: [@AlgTrd_support](URL)"
             }

GREETINGS_2 = {'RU': '\U000026A0 Для активации тестового периода напишите *"буду тестировать"* '
                     'вот сюда \U000027A1 [@AlgTrd_support](URL)',
               'EN': '\U000026A0 To activate your test period send *"will test"* '
                     'to \U000027A1 [@AlgTrd_support](URL)'}


SP = '-'
START_KB_PICS = {'account': u'\U0001F464',
                 'signals': u'\U0001F4E3',
                 'statistics': u'\U0001F4C8',
                 'following': u'\U0001F465',
                 'help': u'\U0001F4AC'}
START_KB = {'account': {'RU': START_KB_PICS['account'] + ' Аккаунт(Оплата)',
                        'EN': START_KB_PICS['account'] + ' Account(Payment)'},
            'signals': {'RU': START_KB_PICS['signals'] + ' Сигналы',
                        'EN': START_KB_PICS['signals'] + ' Signals'},
            'statistics': {'RU': START_KB_PICS['statistics'] + ' Статистика',
                           'EN': START_KB_PICS['statistics'] + ' Statistics'},
            'following': {'RU': START_KB_PICS['following'] + ' Автоследование',
                          'EN': START_KB_PICS['following'] + ' Following'},
            'help': {'RU': START_KB_PICS['help'] + ' Поддержка',
                     'EN': START_KB_PICS['help'] + ' Support'}
            }

BACK_IND = 'back'
BACK_BUTTON = {'RU': 'назад',
               'EN': 'back'}

ACCOUNT_IND = 'account'
ACCOUNT_TEXT = {'RU': 'Выберите пункт меню:',
                'EN': 'Chose menu item:'}
ACCOUNT_KB = {'status': {'RU': 'статус', 'EN': 'status'},
              'payment': {'RU': 'оплата', 'EN': 'payment'},
              'referrals': {'RU': 'рефералы', 'EN': 'referrals'}
              }
ACCOUNT_PICS = {'status': '',
                'payment': '',
                'referrals': ''
                }

STATUS_IND = 'status'
STATUS_TEXT = {'trial': {'RU': 'Тестовый период закончится ',
                         'EN': 'Trial period ends '},
               'paid': {'RU': 'Ваша подписка оплачена до ',
                        'EN': 'Your paid period is before '},
               'expired': {'RU': 'У вас нет действующей подписки',
                           'EN': 'You have no active subscription'}
               }

PAYMENT_IND = 'payment'

PAYMENT_CURRENCY_IND = 'payment_currency'
PAYMENT_CURRENCY_TEXT = {'RU': 'Выберите валюту для оплаты:',
                         'EN': 'Choose payment currency:'}
PAYMENT_CURRENCY_KB = {'BTC': {'RU': 'BTC',
                               'EN': 'BTC'},
                       'ERC20': {'RU': 'USDT ERC20',
                                 'EN': 'USDT ERC20'},
                       'TRC20': {'RU': 'USDT TRC20',
                                 'EN': 'USDT TRC20'}
                       }

PAYMENT_TEXT = {'RU': 'Выберите услугу для оплаты:',
                'EN': 'Choose service for you:'}
PAYMENT_OPTIONS_KB = {'signals': {'RU': 'Оплатить сигналы',
                                  'EN': 'Pay for signals'},
                      'following': {'RU': 'Оплатить автоследование',
                                    'EN': '{Pay for auto following'}}

PACKAGES = {'1_month': {'duration': 1, 'price': 50},
            '3_months': {'duration': 3, 'price': 100}
            }
SIGNALS_PACKAGES_KB = {'1_month': {'RU': '1 месяц - ',
                                   'EN': '1 month - '},
                       '3_months': {'RU': '3 месяца - ',
                                    'EN': '3 months - '}
                       }

FOLLOWING_PACKAGES = {'fp_1': {'duration': 1, 'price': 50},
                      'fp_2': {'duration': 1, 'price': 125},
                      'fp_3': {'duration': 1, 'price': 250},
                      }
FOLLOWING_PACKAGES_KB = {'fp_1': {'RU': '500-999$ - ',
                                  'EN': '500-999$ - '},
                         'fp_2': {'RU': '1000-2499$ - ',
                                  'EN': '1000-2499$ - '},
                         'fp_3': {'RU': '2500-4999$ - ',
                                  'EN': '2500-4999$ - '},
                         'fp_4': {'RU': '5000 и выше - 2.5% от депозита',
                                  'EN': '5000 and more - 2.5% of deposit'}
                         }
VIP_FOLLOWING_TEXT = {'RU': 'По поводу оплаты свяжитесь с @denisarbsys',
                      'EN': 'For payment please contact @denisarbsys'}

CHECKOUT_IND = 'checkout'
CHECKOUT_TEXT = {'RU': f'Для покупки перечислите на счет ',
                 'EN': f'For purchase send to '}
CHECKOUT_KB = {'paid': {'RU': 'Оплатил',
                        'EN': 'Paid'}
               }
TXID_REQUEST = {'RU': 'Следующим сообщением напишите TxID для подтверждения оплаты\n'
                      'Пример: 6c1b9718a0e47f094b98ed3ae8523ef4fcfc56e4596c41f86477e1cf98d0578c \n'
                      'Для подтверждения оплаты с Binance: \nПример Internal transfer: 5924178757',
                'EN': 'Send TxID in the next message'}

INVALID_TXID = {'RU': 'Некорректный TxID. Попробуйте снова.\nДля отмены оплаты нажмите: ',
                'EN': 'Incorrect TxID. Try again.\nTo cancel payment click:'}
ABORT_BUTTON = {'RU': 'отмена',
                'EN': 'cancel'}


PAID_TEXT = {'RU': 'Оплата будет подтверждена в ближайшее время!\n'
                   'Пока Вы можете перейти в свой аккаунт: https://sys.algtrd.com',
             'EN': 'Payment will be confirmed soon'}

REFERRALS_IND = 'referrals'
REFERRALS_TEXT_l1 = {'RU': 'Ваша реферальная ссылка - ',
                     'EN': 'Your referral link - '}
REFERRALS_TEXT_l2 = {'RU': 'Количество рефералов: ',
                     'EN': 'Referrals amount: '}
REFERRALS_TEXT_l3 = {'RU': 'Реферальное вознаграждение: ',
                     'EN': 'Referral bonus: '}

SIGNALS_IND = 'signal'
SIGNALS_TEXT = {'RU': 'Выберите удобные Вам настройки сигналов:',
                'EN': 'Choose your preferred signals settings:'}
SIGNALS_KB = {'exchanges': {'RU': 'биржи', 'EN': 'exchanges'},
              'strategies': {'RU': 'стратегии', 'EN': 'strategies'},
              'currencies': {'RU': 'валюты', 'EN': 'currencies'}
              }
SIGNALS_KB_PICS = {'exchanges': u'\U0001F3E6 ',
                   'strategies': u'\U0001F3AF ',
                   'currencies': u'\U0001F4B2 '}
C_B_BUTTONS = {'checked': u'\U00002705',
               'unchecked': u'\U0000274C'}

EXCHANGES_IND = 'exchanges'
EXCHANGES_TEXT = {'RU': 'С какими биржами вы хотите работать?',
                  'EN': 'Which exchanges would you like to work with?'}
EXCHANGES_KB = {'1': 'Binance',
                '2': 'BitMEX'}

STRATEGIES_IND = 'strategies'
STRATEGIES_TEXT = {'RU': 'По каким стратегиям вы хотите работать?',
                   'EN': 'Which strategies would you like to use?'}
STRATEGIES_KB = {'1': 'Scalp_15m',
                 '2': 'Trend_4h'}
               # '3': 'Shuttle_15m'

CURRENCIES_IND = 'currencies'
CURRENCIES_TEXT = {'RU': 'С какими валютами вы хотите работать?',
                   'EN': 'Which currencies would you like to work with?'}
CURRENCIES_KB = {'1': 'XBT',
                 '2': 'ETH'}

STATISTICS_IND = 'statistics'
STATISTICS_TEXT = {'RU': 'Выберите алгоритм для просмотра статистики:',
                   'EN': 'Choose algorithm to see statistics'}

FOLLOWING_TEXT = {'RU': 'Что бы использовать автоследование перейдите на наш сайт https://sys.algtrd.com',
                  'EN': 'To use following visit our website'}

HELP_TEXT = {'RU': 'Если у вас есть вопросы обращайтесь в @AlgTrd_support',
             'EN': 'If you have questions contact @AlgTrd_support'}

SUBSCRIPTION_EXPIRED = {'RU': 'Срок вашей подписки истек.\n'
                              'Оплатите подписку через меню оплата или свяжитесь со службой поддержки- @AlgTrd_support',
                        'EN': 'Your subscription expired. \n'
                              'Buy subscription in payment menu or contact support.'}

