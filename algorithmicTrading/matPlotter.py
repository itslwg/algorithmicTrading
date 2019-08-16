import matplotlib.pyplot as plt
import pandas as pd
import readData as readData

def matPlotter(ticker_df, ohlc, file_name = None,
               data_dir='../../data/stock_data/', save = False, show = True):
    """ This function plots the specified statistic for the specified ticker
    :param ticker_df: Ticker pandas data frame with ohlc data.
    :type tickers: character list.
    :param ohlc: Statistic to plot. To choose from open, high, low, and close. 
    :type ohlc: string.
    :param file_name: The file name of the saved plot, without file extension.
    :type file_name: string.
    :param data_dir: The data file directory.
    :type name: string. Defaults to  ../../data/stock_data/'
    :param save: If True, plot is saved to disk. Defaults to False.
    :type save: boolean.
    :param show: If True, plot is spawned. Defaults to True
    """
    # Create plot object with ticker_df and ohlc parameter
    plt.plot_date(x=ticker_df['date'], y=ticker_df[ohlc], fmt = '-')
    plt.grid(True)
    if save: plt.savefig(file_name + '.png')
    if show: plt.show()

