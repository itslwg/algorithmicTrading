%%zipline --start 2016-01-01 --end 2017-01-01 -o ./pipeline_ml.pickle
from zipline.api import *
from zipline.pipeline import Pipeline
from zipline.pipeline.data import USEquityPricing
from zipline.pipeline.factors import Returns
from zipline.optimize import *
from customfactor import SimpleMovingAverage, BollingerBands
import numpy as np
import pandas as pd
import sklearn.model_selection as sk
import pyfolio as pf
from sklearn import svm

def initialize(context):
    '''
    initialize

    Zipline built-in. Function called before the start of the algorithm.
    '''
    context.feature_array = None         # To store the features used for training
    context.classifier = None            # To store the classifier algorithm
    context.target = None                # To store the target for fitting the classifier
    context.predictions = None           # To store the model predictions
    context.trading_days = 1             # Used to count the number of trading days
    # Initialize the pipeline
    the_pipeline = make_pipeline()
    attach_pipeline(the_pipeline, 'the_pipeline')
    # Schedule to order stocks every day
    schedule_function(order_assets,
                      date_rule = date_rules.every_day(),
                      time_rule = time_rules.market_open(hours = 1))

def make_pipeline():
    """Returns a pipeline object"""
    # Define common window length and inputs
    window_length = 20
    inputs = [USEquityPricing.close]
    # Define the custom factors for the pipeline
    simple_moving_average = SimpleMovingAverage(window_length = window_length, inputs = inputs)
    bollinger_bands = BollingerBands(window_length = window_length, inputs = inputs)
    daily_percent_change = Returns(inputs = inputs, window_length = 2)
    latest_close = USEquityPricing.close.latest
    return Pipeline(columns = {'simple_moving_average' : simple_moving_average,
                               'bollinger_bands' : bollinger_bands,
                               'latest_close' : latest_close,
                               'daily_percent_change' : daily_percent_change})

def create_target_array(context, data):
    """Creates the target values

    Transforms the latest close from the context.target to target values,
    i.e. growth by 1%.
    """
    outcome = [1 if daily_growth >= 0.02
               else 0
               for daily_growth in context.feature_array.daily_percent_change]
    context.target = np.array(outcome)
    
def train_classifier(context, data, classifier = svm.SVC(gamma=0.001, C=100)):
    """Trains the classifier
    
    Trains the classifier using the context variable feature_array.
    """
    create_target_array(context, data)
    classifier.fit(context.feature_array.drop('daily_percent_change', axis = 1).values, context.target)
    context.classifier = classifier
    
def before_trading_start(context, data):
    """Get pipeline results

    Zipline built-in. Function called before trading starts (called 8.45 am).
    """
    # Get daily pipeline and remove assets with missing data
    context.pipeline_df = pipeline_output('the_pipeline').dropna(axis = 0)
    if context.feature_array is None:
        context.feature_array = context.pipeline_df
    else:
        context.feature_array = pd.concat([context.feature_array, context.pipeline_df])
    if context.trading_days < 3:
        pass
    elif context.trading_days == 3:
        train_classifier(context, data)
    else:
        predictions = context.classifier.predict(context.pipeline_df.drop('daily_percent_change', axis = 1).values)
        context.predictions = pd.Series(predictions, index = context.pipeline_df.index)
    context.trading_days = context.trading_days + 1

def order_assets(context, data):
    """Orders assets according to predictions from pipeline
    
    Sorts the indexes of the predictions, and places order on 
    first five.
    """
    if context.predictions is not None:
        only_growth = context.predictions[context.predictions == 1]
        ordered = only_growth.sort_index(ascending = False)[5:]
        for asset in ordered.index.tolist():
            order(asset, 5)

def create_report(file_name = 'returns.pdf', return_report = False,
                  type_of_report = pf.create_returns_tear_sheet,
                  *args):
    """Creates a portfolio report

    Uses the pyfolio package.

    Args:

        file_name (string): The file name for the portfolio report.

    Returns:
        
        matplotlib.figure.Figure: The portfolio report, if return_report 
                                  is set to True.
        
    """

    portfolio_report = type_of_report(*args,
                                      returns = pd.read_pickle("pipeline_ml.pickle").returns,
                                      return_fig = True)
    portfolio_report.savefig(file_name)
    if return_report: return portfolio_report
