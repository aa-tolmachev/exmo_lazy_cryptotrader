import requests
from psql_methods import access
import json
from datetime import datetime
from datetime import timedelta
from time import sleep
import psycopg2
from pandas import DataFrame
import pandas as pd


#либы для работы с exmo
import sys
import http.client
import urllib
import json
import hashlib
import hmac
import time

PSQL_heroku_keys = access.PSQL_heroku_keys()


#текущая метка времени с минутой часами
def now_str():
    now = datetime.now()
    now_str = str(now.year)+str(now.month if now.month >= 10 else  '0'+str(now.month))+str(now.day if now.day >= 10 else  '0'+str(now.day)) +' '+str(now.hour if now.hour >= 10 else  '0'+str(now.hour)) + str(now.minute if now.minute >= 10 else  '0'+str(now.minute)) + str(now.second if now.second >= 10 else  '0'+str(now.second))
    return now_str

#текущая дата без часов минут
def today_str_func():
    today = datetime.now()
    today_str = str(today.year)+str(today.month if today.month >= 10 else  '0'+str(today.month))+str(today.day if today.day >= 10 else  '0'+str(today.day)) 
    return today_str




def get_tv_main():

    check_at = now_str()

    PSQL_heroku_keys = access.PSQL_heroku_keys()

    interest_coins = ['ETHUSDT' , 'LTCUSDT' , 'EOSUSDT' , 'XRPUSDT' , 'AEBTC']

    url = 'https://scanner.tradingview.com/crypto/scan'

    strong_buy_binance = {"filter":[{"left":"name","operation":"nempty"},{"left":"exchange","operation":"equal","right":"BINANCE"},{"left":"Recommend.All","operation":"nequal","right":0.5},{"left":"Recommend.All","operation":"in_range","right":[0.5,1]}],"options":{"lang":"en"},"symbols":{"query":{"types":[]},"tickers":[]},"columns":["name","close","change","change_abs","high","low","volume","Recommend.All","exchange","description","name","subtype","update_mode","pricescale","minmov","fractional","minmove2"],"sort":{"sortBy":"name","sortOrder":"asc"},"range":[0,150]}

    strong_sell_binance = {"filter":[{"left":"name","operation":"nempty"},{"left":"exchange","operation":"equal","right":"BINANCE"},{"left":"Recommend.All","operation":"nequal","right":-0.5},{"left":"Recommend.All","operation":"in_range","right":[-1,-0.5]}],"options":{"lang":"en"},"symbols":{"query":{"types":[]},"tickers":[]},"columns":["name","close","change","change_abs","high","low","volume","Recommend.All","exchange","description","name","subtype","update_mode","pricescale","minmov","fractional","minmove2"],"sort":{"sortBy":"name","sortOrder":"asc"},"range":[0,150]}

    sell_binane = {"filter":[{"left":"name","operation":"nempty"},{"left":"exchange","operation":"equal","right":"BINANCE"},{"left":"Recommend.All","operation":"nequal","right":0},{"left":"Recommend.All","operation":"in_range","right":[-0.5,0]}],"options":{"lang":"en"},"symbols":{"query":{"types":[]},"tickers":[]},"columns":["name","close","change","change_abs","high","low","volume","Recommend.All","exchange","description","name","subtype","update_mode","pricescale","minmov","fractional","minmove2"],"sort":{"sortBy":"name","sortOrder":"asc"},"range":[0,150]}

    binance_strong_buy_str = requests.post(url, json=strong_buy_binance)
    binance_strong_sell_str = requests.post(url, json=strong_sell_binance)
    binance_sell_str = requests.post(url, json=sell_binane)


    strong_sell_dict =  json.loads(binance_strong_sell_str.text)
    strong_buy_dict = json.loads(binance_strong_buy_str.text)
    sell_dict =  json.loads(binance_sell_str.text)


    name_arr = []
    rating_arr = []
    prc_change_arr = []
    abs_change_arr = []
    high_change_arr = []
    low_change_arr = []


    for coin_dict in strong_sell_dict['data']:
        coin_pair = coin_dict['d'][0]
        if coin_pair in interest_coins:
            name = coin_dict['d'][0]
            prc_change = coin_dict['d'][2]
            abs_change = coin_dict['d'][3]
            high_change = coin_dict['d'][4]
            low_change = coin_dict['d'][5]
            
            name_arr.append(name)
            rating_arr.append('strong_sell')
            prc_change_arr.append(prc_change)
            abs_change_arr.append(abs_change)
            high_change_arr.append(high_change)
            low_change_arr.append(low_change)

    for coin_dict in strong_buy_dict['data']:
        coin_pair = coin_dict['d'][0]
        if coin_pair in interest_coins:
            name = coin_dict['d'][0]
            prc_change = coin_dict['d'][2]
            abs_change = coin_dict['d'][3]
            high_change = coin_dict['d'][4]
            low_change = coin_dict['d'][5]
            
            name_arr.append(name)
            rating_arr.append('strong_buy')
            prc_change_arr.append(prc_change)
            abs_change_arr.append(abs_change)
            high_change_arr.append(high_change)
            low_change_arr.append(low_change)

    for coin_dict in sell_dict['data']:
        coin_pair = coin_dict['d'][0]
        if coin_pair in interest_coins:
            name = coin_dict['d'][0]
            prc_change = coin_dict['d'][2]
            abs_change = coin_dict['d'][3]
            high_change = coin_dict['d'][4]
            low_change = coin_dict['d'][5]
            
            name_arr.append(name)
            rating_arr.append('sell')
            prc_change_arr.append(prc_change)
            abs_change_arr.append(abs_change)
            high_change_arr.append(high_change)
            low_change_arr.append(low_change)



    traiding_view_main_info = pd.DataFrame({'par_name':name_arr,
                                            'rating':rating_arr,
                                            'prc_change':prc_change_arr,
                                            'abs_change':abs_change_arr,
                                            'high_change':high_change_arr,
                                            'low_change':low_change_arr}
                                            )


    if traiding_view_main_info.shape[0] > 0:

        #создаем подключение к PSQL
        conn = psycopg2.connect("dbname='%(dbname)s' port='%(port)s' user='%(user)s' host='%(host)s' password='%(password)s'" % PSQL_heroku_keys)

        # создаем запрос
        cur = conn.cursor()
        
        for i , row in traiding_view_main_info.iterrows():
            insert_dict = dict(row)

            par_name = insert_dict['par_name']
            rating = insert_dict['rating']
            prc_change = insert_dict['prc_change']
            abs_change = insert_dict['abs_change']
            high_change = insert_dict['high_change']
            low_change = insert_dict['low_change']





            #создаем sql иньекцию
            sql_tv = ''.join([

            "insert into exmo_info.traiding_view_main (par_name , check_at , rating , prc_change , abs_change , high_change ,low_change) ",
            "VALUES ('",par_name,"','",check_at,"','",rating,"',",str(prc_change),",",str(abs_change),",",str(high_change),",",str(low_change),")"
            ])

            #создаем запись в exmo_info.ticker
            cur.execute(sql_tv)
            conn.commit()
            sleep(0.1)


        cur.close()
        #закрываем подключение
        conn.close()

            
    return 200