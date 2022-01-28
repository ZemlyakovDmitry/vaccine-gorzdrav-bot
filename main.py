# -*- coding: utf-8 -*-
import json
from threading import Timer

import requests as r

import config as cfg

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36'}
url = "https://gorzdrav.spb.ru/_api/api/v2/schedule/lpu/" + cfg.lpu + "/speciality/" + cfg.speciality + "/doctors"
tg_url = 'https://api.telegram.org/bot' + cfg.token + '/sendMessage'

in_stock = "no"


def bot():
    global in_stock
    resp = r.get(url, headers, timeout=10)
    data = json.loads(resp.text)
    date = data['result'][0]['nearestDate']
    print(date)

    def post():
        r.post(tg_url, data=data, timeout=15)

    if date == None and in_stock == "no":
        in_stock = "no"
        print("not in stock")
        Timer(1800, bot).start()
    elif date != None and in_stock == "no":
        data = {'chat_id': cfg.chat_id, 'text': 'Талоны на вакцинацию появилась. Ближайшая дата вакцинации: ' + date[0:-9]}
        post()
        in_stock = "yes"
        Timer(1800, bot).start()
    elif date == None and in_stock == "yes":
        data = {'chat_id': cfg.chat_id, 'text': 'Талоны на вакцинацию закончилась'}
        post()
        in_stock = "no"
        Timer(1800, bot).start()
    else:
        print("not in stock else")
        Timer(1800, bot).start()


try:
    bot()
except Exception as e:
    print(e)
    Timer(300, bot).start()
