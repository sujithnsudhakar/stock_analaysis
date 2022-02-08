import typing
from unittest import result
import yfinance as yf
import pandas as pd
from datetime import date
import json
import time
import datetime

def select_stock_data_for_company(mysql, company: str, ts_date):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM STOCK_DATA WHERE NAME = %s AND DATE = %s', (company, ts_date))
    row = cur.fetchone()
    return row

def get_stock_info(mysql, company:str, stock_date:str):
    f = '%Y-%m-%d %H:%M:%S'
    ts_date = datetime.datetime.strptime(stock_date, f)
    row = select_stock_data_for_company(mysql, company, ts_date)
    return row
    
def load_data(company:str, start_date, end_date):
    data = yf.download(company, start_date, end_date)
    data.reset_index(inplace=True)
    return data

def insert_data(stock_df, company, mysql):
    for index, row in stock_df.iterrows():
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO STOCK_DATA VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (company, row['Date'], row['Open'], row['High'], row['Low'], row['Close'], row['Volume']))
        mysql.connection.commit()
        cur.close()
    
def persist_fin_data(mysql):
    # TODO get the company and start_date from request param only if we are planning to give an interface
    # company = request.args.get('company')
    company = "GOOG"
    start_date = "2015-01-01"
    end_date = date.today().strftime("%Y-%m-%d")
    stock_df  = load_data(company, start_date, end_date)
    insert_data(stock_df, company, mysql)
    
    
