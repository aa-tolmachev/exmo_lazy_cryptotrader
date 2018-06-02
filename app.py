from flask import Flask
from flask import request
import requests
from flask import make_response
import os
import json
from pandas import DataFrame
import traceback

application = Flask(__name__)  # Change assignment here


# тестовый вывод
@application.route("/")  
def hello():
    return "Hello World!"

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
    application.run(debug=False, port=port, host='0.0.0.0')

