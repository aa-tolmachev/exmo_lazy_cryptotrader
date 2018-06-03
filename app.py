from flask import Flask
from flask import request
import requests
from flask import make_response
import os
import json
from pandas import DataFrame
import traceback

#наши подготовленные либы
from psql_methods import get_exmo_info

application = Flask(__name__)  # Change assignment here


# тестовый вывод
@application.route("/")  
def hello():
    return "Hello World!"


#запись информации по exmo.ticker в нашу бд exmo_info.ticker
@application.route("/get_ticker")  
def get_ticker():
    psql_methods.exmo_get_ticker( key=exmo_key, secret = exmo_sec)
    return "200"

#тест крона
@application.route('/cron_test', methods=['GET', 'POST'])
def cron_test():
    #берем данные из get запроса
    n = request.args.get("n")
    text = str(n)


    return "!",text, 200




if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    exmo_key = os.getenv('exmo_key')
    exmo_sec = os.getenv('exmo_sec')


    get_exmo_info.exmo_get_ticker( key=exmo_key, secret = exmo_sec)
    application.run(debug=False, port=port, host='0.0.0.0')

