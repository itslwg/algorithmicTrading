%%zipline --start 2016-1-1 --end 2018-1-1 -o ../../simulations/ma.pickle

from zipline.api import order, record, symbol, history, order_target
from Asset import Asset
    
def initialize(context):
    '''
    initialize

    Zipline built-in. Function called before trading start.
    '''
    # Get symbols
    context.asset = symbol('AAPL')

def handle_data(context, data):
    '''
    handle_data

    Zipline built-in. Function called every trading day (if daily).
    '''
    # Get 20 day history of data
    stock_history = data.history(context.asset, 'price', bar_count = 50, frequency = '1d')
    # Apply Stock class to data
    stock_instance = Asset('AAPL', daily_adjusted_ohlc = stock_history)
    # Calculate moving average for 20 days
    ma_20 = stock_instance.movingAverage(window = 20)
    ma_50 = stock_instance.movingAverage(window = 50)
    # Order if ma20 > ma50. If less, sell.
    if ma_20 > ma_50:
        order_target(context.asset, 100)
    elif ma_20 < ma_50:
        order_target(context.asset, -100)

    record(asset_price = data.current(context.asset, 'price'),
           ma_20 = ma_20, ma_50 = ma_50)
