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

#информациюя по тикеру
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

#информация по ордер буку
def make_sql_order_book_insert(order_book = None, pair = None):
    
    par_name = pair
    check_at = now_str()
    #ask_quantity - the sum of all quantity values in sell orders
    #ask_amount - the sum of all total sum values in sell orders
    #ask_top - minimum sell price
    #bid_quantity - the sum of all quantity values in buy orders
    #bid_amount - the sum of all total sum values in buy orders
    #bid_top - maximum buy price
    #bid - the list of buy orders where every field is: price, quantity and amount
    #ask - the list of sell orders where every field is: price, quantity and amount
    min_ask = order_book[pair]['ask_top']
    max_bid = order_book[pair]['bid_top']
    price = (float(min_ask) + float(max_bid)) / 2

    bid_df = pd.DataFrame(order_book[pair]['bid'] , columns = ['price' , 'quant' , 'amount'])
    ask_df = pd.DataFrame(order_book[pair]['ask'] , columns = ['price' , 'quant' , 'amount'])


    quant = 0

    w_ask_1 = -1
    l_ask_1 = 0
    w_ask_5 = -1
    l_ask_5 = 0
    w_ask_10 = -1
    l_ask_10 = 0
    w_ask_20 = -1
    l_ask_20 = 0
    w_ask_30 = -1
    l_ask_30 = 0
    w_ask_40 = -1
    l_ask_40 = 0
    w_ask_50 = -1
    l_ask_50 = 0

    for index , row in ask_df.iterrows():
        quant += float(row['quant'])

        if quant >= 1 and w_ask_1 == -1:
            w_ask_1 = sum(ask_df.loc[0:index]['quant'].astype(float) * ask_df.loc[0:index]['price'].astype(float)) / sum(ask_df.loc[0:index]['quant'].astype(float))
            l_ask_1 = index +1

        if quant >= 5 and w_ask_5 == -1:
            w_ask_5 = sum(ask_df.loc[0:index]['quant'].astype(float) * ask_df.loc[0:index]['price'].astype(float)) / sum(ask_df.loc[0:index]['quant'].astype(float))
            l_ask_5 = index +1

        if quant >= 10 and w_ask_10 == -1:
            w_ask_10 = sum(ask_df.loc[0:index]['quant'].astype(float) * ask_df.loc[0:index]['price'].astype(float)) / sum(ask_df.loc[0:index]['quant'].astype(float))
            l_ask_10 = index +1

        if quant >= 20 and w_ask_20 == -1:
            w_ask_20 = sum(ask_df.loc[0:index]['quant'].astype(float) * ask_df.loc[0:index]['price'].astype(float)) / sum(ask_df.loc[0:index]['quant'].astype(float))
            l_ask_20 = index +1

        if quant >= 30 and w_ask_30 == -1:
            w_ask_30 = sum(ask_df.loc[0:index]['quant'].astype(float) * ask_df.loc[0:index]['price'].astype(float)) / sum(ask_df.loc[0:index]['quant'].astype(float))
            l_ask_30 = index +1

        if quant >= 40 and w_ask_40 == -1:
            w_ask_40 = sum(ask_df.loc[0:index]['quant'].astype(float) * ask_df.loc[0:index]['price'].astype(float)) / sum(ask_df.loc[0:index]['quant'].astype(float))
            l_ask_40 = index +1

        if quant >= 50 and w_ask_50 == -1:
            w_ask_50 = sum(ask_df.loc[0:index]['quant'].astype(float) * ask_df.loc[0:index]['price'].astype(float)) / sum(ask_df.loc[0:index]['quant'].astype(float))
            l_ask_50 = index +1



    quant = 0

    w_bid_1 = -1
    l_bid_1 = 0
    w_bid_5 = -1
    l_bid_5 = 0
    w_bid_10 = -1
    l_bid_10 = 0
    w_bid_20 = -1
    l_bid_20 = 0
    w_bid_30 = -1
    l_bid_30 = 0
    w_bid_40 = -1
    l_bid_40 = 0
    w_bid_50 = -1
    l_bid_50 = 0

    for index , row in bid_df.iterrows():
        quant += float(row['quant'])

        if quant >= 1 and w_bid_1 == -1:
            w_bid_1 = sum(bid_df.loc[0:index]['quant'].astype(float) * bid_df.loc[0:index]['price'].astype(float)) / sum(bid_df.loc[0:index]['quant'].astype(float))
            l_bid_1 = index +1

        if quant >= 5 and w_bid_5 == -1:
            w_bid_5 = sum(bid_df.loc[0:index]['quant'].astype(float) * bid_df.loc[0:index]['price'].astype(float)) / sum(bid_df.loc[0:index]['quant'].astype(float))
            l_bid_5 = index +1

        if quant >= 10 and w_bid_10 == -1:
            w_bid_10 = sum(bid_df.loc[0:index]['quant'].astype(float) * bid_df.loc[0:index]['price'].astype(float)) / sum(bid_df.loc[0:index]['quant'].astype(float))
            l_bid_10 = index +1

        if quant >= 20 and w_bid_20 == -1:
            w_bid_20 = sum(bid_df.loc[0:index]['quant'].astype(float) * bid_df.loc[0:index]['price'].astype(float)) / sum(bid_df.loc[0:index]['quant'].astype(float))
            l_bid_20 = index +1

        if quant >= 30 and w_bid_30 == -1:
            w_bid_30 = sum(bid_df.loc[0:index]['quant'].astype(float) * bid_df.loc[0:index]['price'].astype(float)) / sum(bid_df.loc[0:index]['quant'].astype(float))
            l_bid_30 = index +1

        if quant >= 40 and w_bid_40 == -1:
            w_bid_40 = sum(bid_df.loc[0:index]['quant'].astype(float) * bid_df.loc[0:index]['price'].astype(float)) / sum(bid_df.loc[0:index]['quant'].astype(float))
            l_bid_40 = index +1

        if quant >= 50 and w_bid_50 == -1:
            w_bid_50 = sum(bid_df.loc[0:index]['quant'].astype(float) * bid_df.loc[0:index]['price'].astype(float)) / sum(bid_df.loc[0:index]['quant'].astype(float))
            l_bid_50 = index +1

    
    
    if order_book is None:
        return 'code: 400'
    else:
        statement_sql = ''.join([

                'insert into exmo_info.order_book (' , "par_name , check_at , min_ask ,", 
                "max_bid , price , w_ask_1 , l_ask_1 , w_ask_5 , l_ask_5 , w_ask_10, l_ask_10 , w_ask_20,",
                "l_ask_20, w_ask_30, l_ask_30, w_ask_40, l_ask_40, w_ask_50, l_ask_50, w_bid_1, l_bid_1,",
                "w_bid_5, l_bid_5, w_bid_10, l_bid_10, w_bid_20, l_bid_20, w_bid_30, l_bid_30, w_bid_40,",
                "l_bid_40, w_bid_50, l_bid_50)",
                "VALUES ('" , par_name, "','", check_at, "',", str(min_ask) , "," , str(max_bid) , 
                ",", str(price), ",", str(w_ask_1), ",", str(l_ask_1), ",", str(w_ask_5), ",", str(l_ask_5), ",", str(w_ask_10), ",", str(l_ask_10), ",",str(w_ask_20),
                ",", str(l_ask_20) ,",", str(w_ask_30), ",", str(l_ask_30), ",", str(w_ask_40), ",", str(l_ask_40), ",", str(w_ask_50), ",", str(l_ask_50),
                ",", str(w_bid_1),",",str(l_bid_1), ",", str(w_bid_5), ",", str(l_bid_5), ",", str(w_bid_10), ",", str(l_bid_10), ",", str(w_bid_20), ",", str(l_bid_20),
                ",", str(w_bid_30), ",",  str(l_bid_30), ",", str(w_bid_40), ",", str(l_bid_40), ",", str(w_bid_50), ",", str(l_bid_50),  ")"
        ])
    
        return statement_sql


#получаем данные дпо ticker
def exmo_get_ticker(PSQL_heroku_keys = PSQL_heroku_keys , pair = 'ETH_USD', key=None, secret = None):
    ###################

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
    sleep(0.1)
    #создаем sql иньекцию
    sql_ticker = make_sql_ticker_insert(ticker= ticker, pair = 'EOS_USD')
    #создаем запись в exmo_info.ticker
    cur.execute(sql_ticker)
    conn.commit()
    sleep(0.1)
    #создаем sql иньекцию
    sql_ticker = make_sql_ticker_insert(ticker= ticker, pair = 'LTC_USD')
    #создаем запись в exmo_info.ticker
    cur.execute(sql_ticker)
    conn.commit()
    sleep(0.1)
    #создаем sql иньекцию
    sql_ticker = make_sql_ticker_insert(ticker= ticker, pair = 'XRP_USD')
    #создаем запись в exmo_info.ticker
    cur.execute(sql_ticker)
    conn.commit()



    cur.close()
    #закрываем подключение
    conn.close()
    ExmoAPI_instance = None


    ###############

    #получаем информацию по order_book
    params = { "pair" :"ETH_USD",
          "limit" : 1000
         }
    ExmoAPI_instance = ExmoAPI(key, secret)
    order_book = ExmoAPI_instance.api_query('order_book', params )
    ExmoAPI_instance = None


    #создаем подключение к PSQL
    conn = psycopg2.connect("dbname='%(dbname)s' port='%(port)s' user='%(user)s' host='%(host)s' password='%(password)s'" % PSQL_heroku_keys)

    # создаем запрос
    cur = conn.cursor()

    #создаем sql иньекцию
    sql_order_book = make_sql_order_book_insert(order_book = order_book, pair = 'ETH_USD')
    #создаем запись в exmo_info.ticker
    cur.execute(sql_order_book)
    conn.commit()
    sleep(0.1)


    #получаем информацию по order_book
    params = { "pair" :"EOS_USD",
          "limit" : 1000
         }
    ExmoAPI_instance = ExmoAPI(key, secret)
    order_book = ExmoAPI_instance.api_query('order_book', params )
    ExmoAPI_instance = None
    #создаем sql иньекцию
    sql_order_book = make_sql_order_book_insert(order_book = order_book, pair = 'EOS_USD')
    #создаем запись в exmo_info.ticker
    cur.execute(sql_order_book)
    conn.commit()
    sleep(0.1)


    #получаем информацию по order_book
    params = { "pair" :"LTC_USD",
          "limit" : 1000
         }
    ExmoAPI_instance = ExmoAPI(key, secret)
    order_book = ExmoAPI_instance.api_query('order_book', params )
    ExmoAPI_instance = None
    #создаем sql иньекцию
    sql_order_book = make_sql_order_book_insert(order_book = order_book, pair = 'LTC_USD')
    #создаем запись в exmo_info.ticker
    cur.execute(sql_order_book)
    conn.commit()
    sleep(0.1)

    #получаем информацию по order_book
    params = { "pair" :"XRP_USD",
          "limit" : 1000
         }
    ExmoAPI_instance = ExmoAPI(key, secret)
    order_book = ExmoAPI_instance.api_query('order_book', params )
    ExmoAPI_instance = None
    #создаем sql иньекцию
    sql_order_book = make_sql_order_book_insert(order_book = order_book, pair = 'XRP_USD')
    #создаем запись в exmo_info.ticker
    cur.execute(sql_order_book)
    conn.commit()
    sleep(0.1)





    cur.close()
    #закрываем подключение
    conn.close()
    ExmoAPI_instance = None

    return '200'


