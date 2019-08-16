from zipline.pipeline import CustomFactor, Pipeline
from numpy import nanstd
import Asset
import imp
imp.reload(Asset)
from Asset import Asset
import pandas as pd
import numpy as np

'''
Note that the following customfactors are defined for learning purposes.
Most are built-in with zipline pipeline api. 
'''

class StdDev(CustomFactor):
    """Pipeline CustomFactor calculating the standard deviation.

    The CustomFactor used in the pipeline tutorial.

    """
    def compute(self, today, asset_ids, out, values):
        """Calculates the standard deviation for pipeline."""
        out[:] = nanstd(values, ddof = 1, axis=0)

class SimpleMovingAverage(CustomFactor):
    """Pipeline CustomFactor to calculate the simple moving average.

    This can be found as a built-in in the pipeline API.
    """
    params = {'window' : 20}
    window_length = params['window']    
    def compute(self, today, asset_ids, out, close, window):
        """Computes the simple moving average for the asset."""
        asset = Asset(price = close, pipeline = True)
        out[:] = asset.simple_moving_average(window = window)
'''

class ExponentialMovingAverage(CustomFactor):
    
    params = {'window' : 20}
    window_length = params['window']
    def compute(self, today, asset_ids, out, close, window):
        asset = Asset(price = close, pipeline = True)
        out[:] = asset.exponential_moving_average(window = window, return_latest = True)

class Macd(CustomFactor):
    # Params for the EMAs
    params = {'short_ema_period' : 12,
              'long_ema_period' : 26,
              'signal_ema_period' : 9}
    window_length = params['long_ema_period']

    def compute(self, today, asset_ids, out, close,
                long_ema_period, short_ema_period, signal_ema_period):
        """Computes the MACD indicator for each asset in the universe."""
        # Instanstiate the closes as an asset
        asset = Asset(price = close, pipeline = True)
        out[:] = asset.macd(short_ema_period = short_ema_period,
                            long_ema_period = long_ema_period,
                            signal_ema_period = signal_ema_period)
'''
class BollingerBands(CustomFactor):
    """Pipeline customfator for Bollinger Bands.

    This can be found built-in in the pipeline API.

    """
    params = {'window_ma' : 20, 'window_std' : 20}
    def compute(self, today, asset_ids, out, close, window_ma, window_std):
        """Cacluates and returns the bollinger band difference"""
        # Instanstiate close bas asset object
        asset = Asset(price = close, pipeline = True)
        out[:] = asset.bollinger_bands(window_ma = window_ma,
                                       window_std = window_std)

class TenDayLookbackPrice(CustomFactor):
    """Pipeline customfactor for ten day price as features.

    Notice that the n_day_lookback parameter does not work
    properly and does not change if inputed differently.
    For now, ten day price is used.

    """
    params = {'n_day_lookback' : 10}
    window_length = 10
    outputs = [str(i) + '_day_lookback' for i in range(params['n_day_lookback'])]
    def compute(self, today, asset_ids, out, close, n_day_lookback):
        """Returns the price for n days back"""
        for i in range(n_day_lookback):
            setattr(out, str(i) + '_day_lookback', close[i, :])


