import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sklearn.model_selection as sk
from sklearn import svm

class Asset(object):
    
    def __init__(self, price = None, pipeline = False):
        """Init."""
        self.price = price
        # If pipeline, the price object is input as M x N numpy array, where M is
        # window length and N is the number of assets
        self.pipeline = pipeline
        
    def simple_moving_average(self, series = None, window = None, *args):
        """Estimates the simple moving average"""
        if series is None:
            series = self.price
        if window is None:
            window = len(series.index)
        ma = ''
        if not self.pipeline:
            ma = series.rolling(window = window, *args).mean()
        else:
            ma = np.nanmean(series, axis = 0, *args)
        return ma
    
    def exponential_moving_average(self, series = None, window = None,
                                   return_latest = False):
        """Calculates the exponential moving average with pandas .emwa"""
        if series is None:
            series = self.price
        if window is None:
            window = len(self.price.index)
        ema = ''
        # Calculate the exponential moving average over a window period
        if not self.pipeline:
            ema = pd.ewma(series, span = window)#series[-20:].ewma(span = window)
        else:
#            print (np.around(series, decimals = 3)[:, 0])
            as_df = pd.DataFrame(series) # EMA could be vectorized using numpy
            ema_array = as_df.apply(lambda col: pd.ewma(col, span = window)).values
            ema = ema_array[-1] if return_latest else ema_array
#            else:
#                as_pd_series = pd.Series(series)
#                ema = as_pd_series.ewm(span = window).mean()[-1]
        return ema

    def macd(self, short_ema_period = 12, long_ema_period = 26, signal_ema_period = 9):
        """Calculates Moving Average Convergence Divergence. Stockcharts formula."""
        short_ema = self.exponential_moving_average(window = short_ema_period)
        long_ema = self.exponential_moving_average(window = long_ema_period)
        # Define the macd line and the signal line
        macd_line = short_ema - long_ema
        signal_line = self.exponential_moving_average(series = macd_line, window = signal_ema_period)
        macd_hist = macd_line - signal_line if not self.pipeline else (macd_line - signal_line)[-1]
        # Return the macd histogram values
        return macd_hist
        
    def bollinger_bands(self, window_ma = 20, window_std = 20,
                        return_difference = True):
        """Calculates Bollinger Bands."""
        ## Get moving average
        ma = self.simple_moving_average(window = window_ma)
        # Calculate rolling sample standard deviations for upper and lower band
        price_std = ''
        if not self.pipeline:
            price_std = self.price.rolling(window = window_std).std(ddof = 1)
        else:
            price_std = np.nanstd(self.price[-window_std:], axis = 0, ddof = 1)
        # Define names for bands
        lower_band = ma - 2 * price_std
        upper_band = ma + 2 * price_std
        return_object = upper_band - lower_band if return_difference else pd.DataFrame({'lower': lower_band, 'center' : ma,  'upper' : upper_band})
        return return_object

    def split_data(self, window = None):
        """Splits the price data into traininga test datasets."""
        if window is None:
            window = len(self.price.index)
        # Split data to training and test sets
        train, test = sk.train_test_split(self.price.iloc[-window:], test_size = 0.2)

        return train, test

    def setupmodel(*args):
        '''
        setupmodel

        Method to setup e.g. keras model with layers
        '''
        pass

    def feature_setup(self, *features, price_as_feature = True,
                      n_days_lookback = 10):
        """Creates the feature dataset for modelling."""
        # https://stackoverflow.com/questions/22732589/concatenating-empty-array-in-numpy
        # Empty array for features
        feature_array = np.array([])
        for feature in features:
            # Reshape feature series
            feature = feature.values.reshape(-1,1)
            feature_array = np.hstack([feature_array, feature]) if feature_array.size else feature
        if price_as_feature:
            # Init array with repeated (n_days_lookback times) columns of price
            price_features = np.tile(self.price.values.reshape(-1,1), n_days_lookback)
            # Could be vectorized
            for i in range(1, n_days_lookback + 1):
                # From https://stackoverflow.com/questions/30399534/shift-elements-in-a-numpy-array
                # Shift days by iterating over numpy array. Fastest way apparently
                price_features[i:, i - 1] = price_features[:-i, i - 1]
                price_features[:i, i - 1] = np.nan
            feature_array = np.hstack([feature_array, price_features]) if feature_array.size else price_features
        # Extract the rows that does not contain NaNs
        feature_array = feature_array[~np.isnan(feature_array).any(axis = 1)]
        
        return feature_array

    def fit_classifier(self, feature_array, outcome,
                       classifier = svm.SVC(gamma=0.001, C=100),
                       leave_last_row = False):
        """Fits the classifier to the feature_array and returns the classifier."""
        if leave_last_row:
            feature_array = feature_array[:-1]
            outcome = outcome[:-1]
        # Fit classifier
        classifier.fit(feature_array, outcome)
        return classifier
        
    def plotter(self, *args):
        '''
        plotter

        Method to plot time series of ohlc paramter along with different indicators.
        '''
        # Plot additional indicators given in *args
        for arg in args:
            if isinstance(arg, pd.DataFrame):
                [plt.plot_date(the_data[cold]) for col in the_data]
            plt.plot_date(y = arg, x = data['date'], fmt = '-')

        plt.show()
