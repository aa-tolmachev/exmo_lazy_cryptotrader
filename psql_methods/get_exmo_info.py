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

#класс для работы с ексмо апи
class ExmoAPI:
    def __init__(self, API_KEY, API_SECRET, API_URL = 'api.exmo.com', API_VERSION = 'v1'):
        self.API_URL = API_URL
        self.API_VERSION = API_VERSION
        self.API_KEY = API_KEY
        self.API_SECRET = bytes(API_SECRET, encoding='utf-8')

    def sha512(self, data):
        H = hmac.new(key = self.API_SECRET, digestmod = hashlib.sha512)
        H.update(data.encode('utf-8'))
        return H.hexdigest()

    def api_query(self, api_method, params = {}):
        params['nonce'] = int(round(time.time() * 1000))
        params =  urllib.parse.urlencode(params)

        sign = self.sha512(params)
        headers = {
            
            "Content-type": "application/x-www-form-urlencoded",
            "Key": self.API_KEY,
            "Sign": sign
        }
        conn = http.client.HTTPSConnection(self.API_URL)
        conn.request("POST", "/" + self.API_VERSION + "/" + api_method, params, headers)
        response = conn.getresponse().read()

        conn.close()

        try:
            obj = json.loads(response.decode('utf-8'))
            if 'error' in obj and obj['error']:
                print(obj['error'])
                raise sys.exit()
            return obj
        except json.decoder.JSONDecodeError:
            print('Error while parsing response:', response)
            raise sys.exit()

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

def make_sql_ticker_insert(ticker = None, pair = None):

    par_name = pair
    check_at = now_str()
    update_at = str(datetime.fromtimestamp(ticker[pair]['updated']).strftime('%Y%m%d %H%M%S'))
    deal_24h_max = ticker[pair]['high']
    deal_24h_min = ticker[pair]['low']
    deal_24h_avg = ticker[pair]['avg']
    deal_last = ticker[pair]['last_trade']
    vol_24h = ticker[pair]['vol']
    buy_cur_max = ticker[pair]['buy_price']
    sell_cur_min = ticker[pair]['sell_price']
    
    
    if ticker is None:
        return 'code: 400'
    else:
        statement_sql = ''.join([

                'insert into exmo_info.ticker (' , "par_name , check_at , update_at , deal_24h_max ,", 
                "deal_24h_min , deal_24h_avg , deal_last , vol_24h , buy_cur_max , sell_cur_min )", 
                "VALUES ('" , par_name, "','", check_at, "','", update_at , "'," , deal_24h_max , 
                ",", deal_24h_min, ",", deal_24h_avg, ",", deal_last, ",", vol_24h, ",", buy_cur_max, 
                ",", sell_cur_min , ")"
        ])
    
        return statement_sql

#получаем данные дпо ticker
def exmo_get_ticker(PSQL_heroku_keys = PSQL_heroku_keys , pair = 'ETH_USD', key=None, secret = None):
    # получаем информацию по тикеру
    ExmoAPI_instance = ExmoAPI(key, secret)
    ticker = ExmoAPI_instance.api_query('ticker' )
    ExmoAPI_instance = None

    #создаем подключение к PSQL
    conn = psycopg2.connect("dbname='%(dbname)s' port='%(port)s' user='%(user)s' host='%(host)s' password='%(password)s'" % PSQL_heroku_keys)

    # создаем запрос
    cur = conn.cursor()

    #создаем sql иньекцию
    sql_ticker = make_sql_ticker_insert(ticker= ticker, pair = 'ETH_USD')

    #создаем запись в exmo_info.ticker
    cur.execute(sql_ticker)
    conn.commit()

    cur.close()
    #закрываем подключение
    conn.close()
    ExmoAPI_instance = None
    return '200'


