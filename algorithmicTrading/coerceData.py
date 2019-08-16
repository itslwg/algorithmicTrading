# Import packages
import pandas as pd
import matplotlib.dates as mpl
import json
import os
import time
import datetime as dt

def coerceJsonToPandas(data_dict):
    """ This function reads and coerces ticker data to pandas data frames.
    :param data_dict: Ticker data dictionary.
    :type tickers: character list.
    :param data_dir: The data file directory.
    :type name: string. Defaults to  ../../data/stock_data/'
    :returns: The stock data as pandas data frame.
    """
    # Create df, and transpose
    data_df = pd.DataFrame(data_dict['Time Series (Daily)']).transpose()
    # Convert columns to numeric
    for header in list(data_df):
        # Split header at space, and assign only ohlc parameter as header
        new_header = header.split(" ")[1]
        # Use new header and convert ohlc to numeric
        data_df[new_header] = pd.to_numeric(data_df[header])
        # Drop old col
        data_df = data_df.drop(header, axis=1)
    # Create column of indexes, convert to datetime
    data_df['date'] = [dt.datetime.strptime(date, '%Y-%m-%d') for date in list(data_df.index)]
    # then to matplotlib format - date2num
    # https://stackoverflow.com/questions/1574088/plotting-time-in-python-with-matplotlib
    data_df['date'] = mpl.date2num(data_df['date'])
        
    return (data_df)
