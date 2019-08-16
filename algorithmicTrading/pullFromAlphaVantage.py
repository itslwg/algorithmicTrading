# Import packages
import bs4
import requests
import saveOrPickle
from Stock import Stock
from coerceData import coerceJsonToPandas
import json
import pandas as pd
import time
import os

def getApiKey(file_dir = "../../data/keys.txt"):
    """ Reads API key.
    :param file_dir: The data file directory
    :type name: string. Defaults to "../../data/keys.txt"
    :returns: The API key as string.
    """
    # Read the key_file
    f = open(file_dir, 'r')
    read_f = f.readlines()
    # Stringfy
    stringed = ''.join(read_f)
    # Remove all before first single quotation
    subbed = stringed.split('\'')
    # Return key as string 
    return (subbed[-2])

def pullFromAlphaVantage(ticker,
                           data_folder =  '../../data/stock_data/',
                           stock_instance_dir = '../../data/Stock_instances/', save = True,
                           save_stock_instance = True, to_return = None):
    """ This function pulls ticker history data
    from Alpha Vantage.
    :param ticker: Stock ticker.
    :type ticker: string.
    :param data_folder: The directory in which the data is to be stored. Defaults to'../../data/stock_data/'
    :type data_folder: string
    :param stock_instance_dir: The directory in which the instances of the Stock class is to be stored. Defaults to '../../data/Stock_instances/'
    :type stock_instance_dir: string.
    :param save: If True, ticker data is saved to disk. Defaults to True.
    :type save: boolean.
    :param save_stock_instance: If True, ticker is saved to disk as Stock class.
p    :param to_return: If True, ticker dict is returned. Defaults to True.
    :type to_return: boolean.
    :returns: JSON formatted ticker data.
    """
    # Get API key
    api_key = getApiKey()
    # Define generalized url to Alpha Vantage
    alpha_url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=TICKER&outputsize=full&apikey=APIKEY'
    # Replace TICKER and APIKEY keywords in the url,
    # could have used params in requests
    ticker_url = alpha_url.replace('TICKER', ticker).replace('APIKEY', api_key)
    # Pull ticker data as json, and parse
    data_dict = requests.get(ticker_url).json()
    # Coerce json data to pandas DataFrame
    data_df = coerceJsonToPandas(data_dict=data_dict)
    # Instance Stock class
    stock_instance = Stock(ticker=ticker, daily_ohlc=data_df, daily_adjusted_ohlc='')
    # Save ticker data to data_folder, if Save
    if save: saveOrPickle.saveData(ticker=ticker,
                                   data_dict=data_dict,
                                   data_folder=data_folder)
    # Save ticker data as Stock class instance, if save_stock_instance
    if save_stock_instance: saveOrPickle.pickleStockInstance(ticker=ticker,
                                                             stock_class_instance=stock_instance,
                                                             stock_instance_dir=stock_instance_dir)
    # Return if return
    if to_return is not None:
        if to_return == "instance": return_object = stock_instance
        if to_return == "raw": return_object = data_dict
        
        return (return_object)
