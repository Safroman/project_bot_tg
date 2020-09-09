#!/usr/bin/env python
#
#   Processing signals from Web Hooks
#
#
#   Denis Yasman
#
#   13.07.2020

from PIL import Image, ImageDraw, ImageFont
import requests
import datetime
from datetime import timezone
import os
import configparser
import re


def create_config(path):
    """
    Create a config file
    """
    config = configparser.ConfigParser()
    config.add_section("Settings")
    config.set("Settings", "signal_number", "1")
    with open(path, "w") as config_file:
        config.write(config_file)


def get_config(path):
    """
    Returns the config object
    """
    if not os.path.exists(path):
        create_config(path)

    config = configparser.ConfigParser()
    config.read(path)
    return config


def get_setting(path, section, setting):
    """
    Print out a setting
    """
    config = get_config(path)
    value = config.get(section, setting)
    msg = "{section} {setting} is {value}".format(
        section=section, setting=setting, value=value
    )

    print(msg)
    return value


def update_setting(path, section, setting, value):
    """
    Update a setting
    """
    config = get_config(path)
    config.set(section, setting, value)
    with open(path, "w") as config_file:
        config.write(config_file)


def delete_setting(path, section, setting):
    """
    Delete a setting
    """
    config = get_config(path)
    config.remove_option(section, setting)
    with open(path, "w") as config_file:
        config.write(config_file)




SIGNAL_TEMPLATE = 'images/signal_template.png'
BOT_TOKEN = '1341976392:AAEW3pLeimE5dJU6P7EHlGv7zYfUYvFWa5g'
CHANEL_ID = '@AlgTrd_Signals'
URL_TEL_API_BASE = 'https://api.telegram.org/bot'
URL_TEL_API_SEND_PHOTO = URL_TEL_API_BASE + BOT_TOKEN + '/sendPhoto'
FONT_COMPUTER = 'computer-says-no.ttf'
CONFIG_FILE = 'setting.ini'
SIGNAL_IMAGES_FOLDER = 'signal_images/'
SIGNALS_LOG = 'signals.txt'
if not os.path.exists(CONFIG_FILE):
    create_config(CONFIG_FILE)





def createImagebySignal(exchange,strategy,pair,signal,enter,tp1,tp2,sl):
    img = Image.open(SIGNAL_TEMPLATE)
    idraw = ImageDraw.Draw(img)
    font66 = ImageFont.truetype(FONT_COMPUTER, size=66)
    font100 = ImageFont.truetype(FONT_COMPUTER, size=100)
    signal_number = str(get_setting(CONFIG_FILE, 'Settings', 'signal_number'))
    signal_line = 'SIGNAL ' + signal_number
    strategy_line = 'Strategy: ' + strategy
    idraw.text((((img.size[0] - font100.getsize(signal_line)[0]) / 2), 40), signal_line, font=font100)
    idraw.text((((img.size[0] - font66.getsize(strategy_line)[0]) / 2), 120), strategy_line, font=font66)
    dt_str = 'Date: '+datetime.datetime.now(tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S")+' UTC'
    idraw.text((((img.size[0] - font66.getsize(dt_str)[0]) / 2), 172),dt_str, font=font66)
    if signal == 'Long':
        arrow = Image.open('long.png')
    else:
        arrow = Image.open('Short.png')
    idraw.text((61, 249), 'Exchange: '+exchange, font=font66)
    idraw.text((550, 249), 'STOP-LOSS: '+sl, font=font66)
    idraw.text((61, 299), 'Pair: '+pair, font=font66)
    idraw.text((61, 349), 'Side: '+signal, font=font66)
    img.paste(arrow, (300, 339), mask=arrow)
    idraw.text((61, 399), 'Enter: '+enter, font=font66)
    idraw.text((61, 449), 'TP1: '+tp1, font=font66)
    idraw.text((61, 499), 'TP2: '+tp2, font=font66)
    img_name = strategy+'_'+dt_str+'_'+signal+'.png'
    img.save(SIGNAL_IMAGES_FOLDER+img_name)
    dt = datetime.datetime.now(tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    f = open(SIGNALS_LOG,'a')
    f.write(signal_number+';'+exchange+';'+strategy+';'+dt+';'+pair+';'+signal+';'+enter+';'+tp1+';'+tp2+';'+sl+'\n')
    f.close()
    return img_name

def postImagetoTelegrammChanel(signal_file):
    #result = requests.post(URL_TEL_API_SEND_PHOTO, data={'chat_id': CHANEL_ID}, files={'photo': open(signal_file, 'rb')})
    signal_number = int(get_setting(CONFIG_FILE, 'Settings', 'signal_number'))
    signal_number = signal_number + 1
    update_setting(CONFIG_FILE, 'Settings', 'signal_number', str(signal_number))
    return result




def application(environ, start_response):
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
        request_body_size = 0
    request_body = environ['wsgi.input'].read(request_body_size)

    f = open("post_arguments.txt", "a")
    dt_str = 'Date: '+datetime.datetime.now(tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S")+' UTC'
    f.write(dt_str+" >> "+str(request_body)+'\n')
    f.close()

    webhook = str(request_body)
    exchange = re.findall(r'exchange=(\w+)', webhook)[0]
    strategy = re.findall(r'strategy=(\w+)', webhook)[0]
    pair = re.findall(r'pair=(\w+)', webhook)[0]
    signal = re.findall(r'signal=(\w+)', webhook)[0]
    try:
        tp1 = re.findall(r'tp1=([\w.]+)', webhook)[0]
    except:
        tp1 = 0

    try:    
        tp2 = re.findall(r'tp2=([\w.]+)', webhook)[0]
    except:
        tp2 = 0

    sl = re.findall(r'sl=([\w.]+)', webhook)[0]

    try:
        enter = re.findall(r'enter=([\w.]+)', webhook)[0]
    except:
        enter = 0

    if signal != 'update':
        signal_file = createImagebySignal(exchange, strategy, pair, signal, enter, tp1, tp2, sl)
        postImagetoTelegrammChanel((SIGNAL_IMAGES_FOLDER + signal_file))

        params = {'signal_path': '',
                  'exchange': exchange,
                  'strategy': strategy,
                  'pair': pair}
        requests.post('https://sys.algtrd.com/initiator/send_signal', data=params)

    start_response('200 OK', [('Content-Type', 'text/html')])
    return [b'OK']

