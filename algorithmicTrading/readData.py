# Import packages
import pandas as pd
import matplotlib.dates as mpl
import json
import os
import time
import datetime as dt
import pickle
from pullFromAlphaVantage import pullFromAlphaVantage

def retrieveRawData(ticker, ticker_file,
                    data_dict, data_folder,
                    file_format = 'json'):
    """ Retrieves data from the given dir and appends to the given data_dict.
    :param ticker: Stock ticker.
    :type ticker: string.
    :param ticker_dir: Ticker directory.
    :type tickers: string.
    :param data_dict: The dict to store ticker data
    :type name: dictionary.
    :param file_format: Type of data file. Defaults to 'json'. Options are 'json' or 'csv'
    :type file_format: string.
    """
    if file_format == 'json':
        with open(data_folder + ticker_file, opener) as infile:
            infile = ""
            if file_format == 'csv':
                pass
            elif file_format == 'json':
                infile = json.load(infile)
            data_dict[ticker] = infile
            print (ticker + ' data retrieved from data_dir')
            
def retrievePickledData(ticker, stock_instance_file,
                        stock_instances_folder = '../../data/Stock_instances/'):
    """ Loads pickled data from the given dir.
    :param ticker: Stock ticker.
    :type ticker: string.
    :param stock_instance_dir: 
    :type tickers: string.
    :param all_instances_dir: The folder in which all instances are stored.
    :type all_instances_dir: string.
    """
    # Read pickled data
    with open(stock_instances_folder + stock_instance_file, 'rb') as infile:
        infile = pickle.load(infile)
        print (ticker + ' Stock instance retrieved.')
        
        return (infile)

def readData(tickers,
             data_folder = '../../data/stock_data/',
             stock_instances_folder = '../../data/Stock_instances/',
             offline = True, file_format = 'json'):
    """ Pulls fresh data to raw data folder (if needed), and reads stock instance
    data.
    :param tickers: Stock tickers.
    :type tickers: character list.
    :param data_dir: The data file directory.
    :type name: string. Defaults to  ../../data/stock_data/'
    :param stock_instances_folder: The stock instance directory.
    :type stock_instances_folder: string.
    :param file_format: Type of data file. Defaults to 'json'. Not fully integrated. Passed to retrieveData.
    :type file_format: string.
    """
    # Define printing function for offline parameter
    def offline_printer():
        print ('Parameter offline is True. Change to False to download ticker data!')
    # Initialize dict to ponpulate with Stock instances
    ticker_dict = {}
    # Check if data directory is empty
    if not os.listdir(data_folder): 
        print (data_folder + ' empty...')
        if offline:
            offline_printer()
        else:
            for ticker in tickers:
                print  ('Filling with data from ' + ticker)
                # Fill with raw ticker data; fill stock instances dir with
                # Stock instances; Populate ticker dict with Stock instances
                ticker_dict[ticker] = pullFromAlphaVantage(ticker,
                                                           data_folder = data_folder,
                                                           to_return= 'instance')
    else:
        # Get all paths in the data_folder
        ticker_dirs = os.listdir(data_folder)
        for ticker in tickers:
            # Grep file directory of ticker in the data directory
            raw_file_name = "".join([ticker_dir for ticker_dir in ticker_dirs if ticker in ticker_dir])
            # Remove file extension for reading pickled data
            instance_file_name = raw_file_name.replace('.' + file_format, "")
            # If data for the ticker does not exist, pull from alpha
            if not raw_file_name:
                print (ticker + ' not in raw data folder...')
                if offline:
                    offline_printer()
                else:
                    ticker_dict[ticker] = pullFromAlphaVantage(ticker, 
                                                               data_folder=data_folder,
                                                               to_return='instance')
            else:
                splt_ticker_dir = raw_file_name.split(".")[0].split("_") # Strip file ext, and split
                date = splt_ticker_dir[1]                                # Subset date
                if date != time.strftime("%d%m%Y"):                      # Check if date relev. data
                    if offline:
                        print ('Data not updated for current date, yet offline parameter is True')
                        print ('Reading Stock instance last updated ' + date)
                        ticker_dict[ticker]= retrievePickledData(ticker=ticker,
                                                                 stock_instance_file=instance_file_name,
                                                                 stock_instances_folder=stock_instances_folder)
                    else: 
                        print ('Data old. Replacing data for ' + ticker + " ...")
                        # Remove old raw data file and stock instance dir
                        for folder_dir, the_file_name in zip([data_folder, stock_instances_folder],
                                                             [raw_file_name, instance_file_name]):
                            os.remove(folder_dir + the_file_name)
                        # Retrieve data
                        ticker_dict[ticker] = pullFromAlphaVantage(ticker=ticker,
                                                                  data_folder=data_folder,
                                                                   to_return='instance')
                        print(ticker + " Stock instance retrieved from disk.")
                else:
                    # Retrieve Stock instance
                    ticker_dict[ticker] = retrievePickledData(ticker=ticker,
                                                              stock_instance_file=instance_file_name,
                                                              stock_instances_folder=stock_instances_folder)
            
    return (ticker_dict)

