%%zipline -s 2014-12-17 -e 2014-12-17 -o ../../simulations/pipe.py
from zipline.api import *
from zipline.pipeline import CustomFactor, Pipeline
from zipline.pipeline.data import USEquityPricing
from zipline.pipeline.engine import PipelineEngine
import customfactor
import imp
imp.reload(customfactor)
from customfactor import *
import numpy as np

def initialize(context):
    my_pipe = make_pipeline()
    attach_pipeline(my_pipe, 'my_pipeline')

def compute_target_weights(context, data):
    """Computes the ordering weights from the pipeline securities. 

    From Tutorial.
    """
    # Initialize empty target weights dictionary.
    # This will map securities to their target weight.
    weights = {}

    # If there are securities in our longs and shorts lists,
    # compute even target weights for each security.
    if context.longs and context.shorts:
        long_weight = 0.5 / len(context.longs)
        short_weight = -0.5 / len(context.shorts)
    else:
        return weights

    # Exit positions in our portfolio if they are not
    # in our longs or shorts lists.
    for security in context.portfolio.positions:
        if security not in context.longs and security not in context.shorts and data.can_trade(security):
            weights[security] = 0

    for security in context.longs:
        weights[security] = long_weight

    for security in context.shorts:
        weights[security] = short_weight

    return weights
        
def make_pipeline():
#    stdev = StdDev(inputs = [USEquityPricing.close], window_length = 5)
#    macd = Macd(inputs = [USEquityPricing.close], window_length = 26)
#    exp = ExponentialMovingAverage(inputs = [USEquityPricing.close], window_length = 20)
#    ma = SimpleMovingAverage(inputs = [USEquityPricing.close], window_length = 20)
    bbs = BollingerBands(inputs = [USEquityPricing.close], window_length = 20)
    nday = TenDayLookbackPrice(inputs = [USEquityPricing.close], window_length = 10)
    return Pipeline(columns = {'bbs' : bbs,
                               'nday' : nday})

def before_trading_start(context, data):
    """Zipline built-in.

    Called before trading start.

    """
    def tuples_to_columns(tuple_column_label, new_column_labels, df):
        """Transforms column of tuples to multiple columns.

        See https://stackoverflow.com/questions/25559202/from-tuples-to-multiple-columns-in-pandas.

        Args:
            new_col_list: List of strings. The labels of the columns to be created.

        Returns:
            pandas.DataFrame: The data frame without the original tuple column.

        """
        for index, column_label in enumerate(new_column_labels):
            df[column_label] = df[tuple_column_label].apply(lambda tuple_label: tuple_label[index])
        return df.drop(tuple_column_label, axis = 1)
    context.output = pipeline_output('my_pipeline')
    new_column_labels = ['price_' + str(i) + '_back' for i in reversed(range(1,11))]
    pipe = tuples_to_columns(tuple_column_label = 'nday',
                                        new_column_labels = new_column_labels,
                                        df = context.output)
    # Convert 10 day price to 
#    print (context.output)
#import quantopian.algorithm as algo
#from quantopian.pipeline import Pipeline
#
#def initialize(context):
#    my_pipe = make_pipeline()
#    algo.attach_pipeline(my_pipe, 'my_pipeline')
#
#def make_pipeline():
#    return Pipeline()
#
#def before_trading_start(context, data):
#    # Store our pipeline output DataFrame in context.
#    context.output = algo.pipeline_output('my_pipeline'
