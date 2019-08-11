import requests
from psql_methods import access
import json
from datetime import datetime
from datetime import timedelta
from time import sleep
import psycopg2
from pandas import DataFrame
import pandas as pd
import traceback

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




def main():

    check_at = now_str()

    PSQL_heroku_keys = access.PSQL_heroku_keys()



    #создаем подключение к PSQL
    conn = psycopg2.connect("dbname='%(dbname)s' port='%(port)s' user='%(user)s' host='%(host)s' password='%(password)s'" % PSQL_heroku_keys)

    # создаем запрос
    cur = conn.cursor()



    cur_trade_state = ' '.join([
                "select mt.par_name", "\n"
                ",mt.max_check_at", "\n"
                ",round(mt_info.deal_last / mt_info.deal_24h_avg , 2) as cur_state","\n"
                ",mt_info.deal_last","\n"
                ",case when round(mt_info.deal_last / mt_info.deal_24h_avg , 3) <= 0.98 then 1 else 0 end as factor1_buy","\n"
                ", case when round(mt_info.deal_last / mt_info.deal_24h_avg , 3) <= 0.98 then mt_info.deal_last * 1.015 else null end as factor1_sellprice", "\n"
                "from ","\n"
                "--информация по максимальному состоянию","\n"
                "(","\n"
                "select par_name","\n"
                ",max(check_at) as max_check_at","\n"
                "from exmo_info.ticker","\n"
                "group by par_name","\n"
                ") as mt","\n"
                "left join exmo_info.ticker as mt_info on mt.par_name = mt_info.par_name","\n"
                "and mt.max_check_at = mt_info.check_at"
                
                ])


    probability_of_states = ' '.join([
                "select hy.par_name", "\n",
                ",hy.cur_state", "\n",
                ",round(sum(hy.is_price_up) / sum(1.) , 2) as cur_state_price_up_prob", "\n",
                ",round(sum(hy.is_factor1_up) / sum(1.) , 2) as cur_state_factor_up_prob", "\n",
                ",sum(1) as cnt_cases", "\n",
                "from(", "\n",
                "select p.par_name", "\n",
                ",round(p.deal_last / p.deal_24h_avg , 2) as cur_state", "\n",
                ",p.check_at", "\n",
                ",p.check_at + interval '2' day as end_date_order", "\n",
                ",p.deal_last", "\n",
                ",sum(case when pf.deal_last >= p.deal_last * 1.015 then 1 else 0 end) as cnt_price_up", "\n",
                ",sum(case when round(pf.deal_last / pf.deal_24h_avg , 3) >= round(p.deal_last / p.deal_24h_avg , 3) + 0.015 then 1 else 0 end) as cnt_factor1_up", "\n",
                ",max(case when pf.deal_last >= p.deal_last * 1.015 then 1 else 0 end) as is_price_up", "\n",
                ",max(case when round(pf.deal_last / pf.deal_24h_avg , 3) >= round(p.deal_last / p.deal_24h_avg , 3) + 0.015 then 1 else 0 end) as is_factor1_up", "\n",
                ",max(pf.deal_last) as max_future_deal", "\n",
                ",sum(1) as cnt_trys", "\n",
                "from exmo_info.ticker as p", "\n",
                "left join exmo_info.ticker as pf on p.par_name = pf.par_name", "\n",
                "and pf.check_at > p.check_at", "\n",
                "and pf.check_at < p.check_at + interval '2' day ", "\n",
                "where p.check_at > now() - interval '180' day", "\n",
                "and p.check_at < now() - interval '2' day", "\n",
                "group by 1 , 2 , 3 , 4 , 5", "\n",
                "order by p.check_at", "\n",
                ") as hy", "\n",
                "group by 1 , 2 ", "\n",
                "order by 1 , 2", "\n",
        
                
                ])



    cur.execute(cur_trade_state)
    df_cur_state = pd.DataFrame(cur.fetchall(), columns=[desc[0] for desc in cur.description])

    cur.execute(probability_of_states)
    df_state_probs = pd.DataFrame(cur.fetchall(), columns=[desc[0] for desc in cur.description])



    cur.close()
    #закрываем подключение
    conn.close()


    #смотрим априорную вероятность увеличения стоимости в течение 2-х дней на 1.5%
    cur_state_probability = pd.merge(df_cur_state
             ,df_state_probs
             ,how = 'left'
             ,left_on = ['par_name' , 'cur_state']
             ,right_on = ['par_name' , 'cur_state']
            )

    cur_state_probability.fillna('unknown' , inplace = True)


    result_to_send = cur_state_probability.to_json(orient='records')

    url = 'https://fin-budg-bot.herokuapp.com/external_receive'

    try:
        r = requests.post(url, json=result_to_send)
    except:
        r = 'bad'
        print(r)


    return 200