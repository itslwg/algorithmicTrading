%%zipline -s 2016-01-01 -e 2018-01-01 -o ../../simulations/bb_strategy.pickle
from zipline.api import order, order_target, record, symbol
from Asset import Asset

def initialize(context):
    '''
    initialize

    Zipline built-in. Function called before trading start.
    '''
    context.asset = symbol('AAPL')

def handle_data(context, data):
    '''
    handle_data

    Zipline built-in. Function called every trading day (if daily).
    '''
    # Get 20 day stock history
    stock_history = data.history(context.asset, fields='price', bar_count=20, frequency='1d')
    # Create Stock instance
    stock_instance = Asset('AAPL', daily_adjusted_ohlc = stock_history)
    # Calculate bands
    lower, upper = stock_instance.bollingerBands(window = 20)
    # Define strategy
    if data.current(context.asset, 'price') < lower:
        order_target(context.asset, 100)
    elif data.current(context.asset, 'price') > upper:
        order_target(context.asset, 0)

    record(asset_price = data.current(context.asset,'price'),
           lower_band = lower,
           upper_band = upper)
