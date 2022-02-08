from logging import debug
from flask import Flask, render_template, jsonify
from flask import request
from stock_business import get_stock_info, load_data, persist_fin_data
from flask_cors import CORS

from flask_mysqldb import MySQL
import json

import pandas as pd


app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'stock_analysis'

mysql = MySQL(app)
CORS(app)


@app.route('/')
def index():
    return "success"
    # return render_template('home.html')

@app.route('/getStocks')
def get_stocks():
    # fetch vals from query param ?company=some-value&stock_dt="2021-11-12 00:00:00"
    # sample request http://127.0.0.1:5000/getStocks?company=GOOG&stock_dt=2021-11-12%2000:00:00
    company = request.args.get('company')
    stock_date = request.args.get('stock_dt')
    stock_details = get_stock_info(mysql, company, stock_date)
    return jsonify({"stock_info" :  stock_details})

@app.route('/loadYFinanceData')
def load_stocks_info_into_db():
    persist_fin_data(mysql)
    return "success"


if __name__ == '__main__':
    app.run(debug=True)
