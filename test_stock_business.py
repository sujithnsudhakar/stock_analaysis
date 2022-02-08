from stock_business import get_stock_info, load_data
from flask import Flask
from datetime import date
import datetime
import pytest
from flask_mysqldb import MySQL
from unittest import mock
import pandas as pd


def test_load_data_yields_correct_stock_info_for_correct_time_period():
    company = "AMZN"
    # start date here is a day after start date, e.g. for 15th Dec, we get data from 14th dec
    start_date = "2021-12-15"
    # Excludes end date
    end_date = "2021-12-16"

    f = '%Y-%m-%d %H:%M:%S'
    ts_start_date = datetime.datetime.strptime("2021-12-14 00:00:00", f)
    ts_end_date = datetime.datetime.strptime("2021-12-15 00:00:00", f)

    stock_df  = load_data(company, start_date, end_date)
    assert stock_df['Date'][0] == ts_start_date
    assert stock_df['Date'][1] == ts_end_date

def test_load_data_yields_correct_open_close_values_information():
    company = "AMZN"
    # start date of data is set to the day before the below date, e.g. for 15th Dec, we get data from 14th dec
    start_date = "2021-12-15"
    # Excludes end date
    end_date = "2021-12-16"

    stock_df  = load_data(company, start_date, end_date)

    assert stock_df['Open'][0] == pytest.approx(3351.000000, 0.001)
    assert stock_df['Open'][1] == pytest.approx(3371.959961, 0.001)

    assert stock_df['Close'][0] == pytest.approx(3381.830078, 0.001)
    assert stock_df['Close'][1] == pytest.approx(3466.300049, 0.001)

def test_load_data_yields_correct_high_low_values_information():
    company = "AMZN"
    # start date here is a day after start date, e.g. for 15th Dec, we get data from 14th dec
    start_date = "2021-12-15"
    # Excludes end date
    end_date = "2021-12-16"

    stock_df  = load_data(company, start_date, end_date)

    assert stock_df['High'][0] == pytest.approx(3389.97998, 0.001)
    assert stock_df['High'][1] == pytest.approx(3472.00000, 0.001)

    assert stock_df['Low'][0] == pytest.approx(3328.800049, 0.001)
    assert stock_df['Low'][1] == pytest.approx(3303.899902, 0.001)

def test_load_data_yields_all_required_columns():
    company = "AMZN"
    # start date here is a day after start date, e.g. for 15th Dec, we get data from 14th dec
    start_date = "2021-12-15"
    # Excludes end date
    end_date = "2021-12-16"

    stock_df  = load_data(company, start_date, end_date)
    # TODO try to do prediction including volume, future options influence
    expected_col_names = ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
    cols = stock_df.columns

    assert len(cols) == len(expected_col_names)
    assert all([a == b for a, b in zip(cols, expected_col_names)])

@mock.patch('stock_business.select_stock_data_for_company', return_value = ("GOOG", "2021-12-14 00:00:00", 3351.000000, 3389.97998, 3328.800049, 3381.830078, 3200, 56000))
def test_get_stock_info_yields_correct_values(mock_check_output):
    result = get_stock_info('dummy_sql_connection', 'GOOG', '2021-11-14 00:00:00')
    assert result[0] == "GOOG"
    assert result[1] == "2021-12-14 00:00:00"
    assert result[2] == 3351.000000
    assert result[3] == 3389.97998
    assert result[4] == 3328.800049
    assert result[5] == 3381.830078
    assert result[6] == 3200
    assert result[7] == 56000

# TODO test the end point itself by creating a dummy client
# def test_base_route():
#     app = Flask(__name__)
#     client = app.test_client()
#     url = '/'

#     response = client.get(url)
#     assert response.get_data() == b'success'
#     assert response.status_code == 200





