%%zipline -s 2014-12-17 -e 2014-12-17 -o ../../simulations/ml.pickle

from zipline.api import order, order_target, record, symbol, date_rules, time_rules, schedule_function
import numpy as np
import Asset
import imp
imp.reload(Asset)
from Asset import Asset

# Define the n day price to use as features
n_day_lookback = 20
window_ma = 20
window_std = 20

def initialize(context):
    """Zipline built-in. Function called before trading start."""
    context.first_day = True
    # Pipeline asset data
    the_pipeline = make_pipeline()
    attach_pipeline(my_pipe, 'the_pipeline')
    # Schedule order assets to run just before close; not ideal in real life, as it maybe is not filled
    # schedule_function(order_assets)
    # Schedule to train the model every month
    schedule_function(func = train_classifier, date_rule = date_rules.month_end(),
                      time_rule = time_rules.market_open(hours = -1))

def getAndSetAsset(context, data, bar_count):
    """Retrieves asset data and instantiates asset class."""
    # Get asset history
    asset_history = data.history(context.assets, 'close', bar_count = bar_count,
                                 frequency = "1d")
    # Create Asset instance
    asset =  Asset(price = asset_history[:-1])
    return asset, asset_history

def setFeatures(context, data, bar_count):
    """Create the feature set and set the outcome."""
    # Get asset history and set as asset class.
    asset, asset_history = getAndSetAsset(context, data, bar_count = bar_count)
    # Create feature setb
    feature_array = asset.feature_setup(asset.simple_moving_average(window = 20),
                                        asset.bollinger_bands(window_ma = window_ma, window_std = window_std),
                                        n_days_lookback = n_day_lookback)
    return asset, feature_array
    
def train_classifier(context, data):
    """Trains the model on a subset of data. To be scheduled."""
    asset, feature_array = setFeatures(context, data, bar_count = 100)
    # Create binary outcome from prices
    growth = asset.price.pct_change()[n_day_lookback:]
    outcome = np.array([1 if daily_growth >= 0.01 else 0 for daily_growth in growth])
    classifier = asset.fit_classifier(feature_array = feature_array, outcome = outcome, leave_last_row = True)
    # predicted_value = asset.fitAndPredictWithClassifier(feature_array = features, outcome = outcome)
    # Set context variable to classifier
    context.classifier = classifier
    return feature_array
    
def order_assets(context, data):
    """Long assets"""
    '''
    # Get features that were used to train the classifier
    asset, feature_array = setFeatures(context, data, bar_count = 30)
    # Set features
    expected_to_grow = context.classifier.predict(np.array(feature_array[-1:]))
    '''
    for asset in symbols(context.assets):
        order(asset, 5)

def make_pipeline():
    """Instantiates a pipeline object

    Calculates bollingerbands, 10-day lookback price, and simple MA
    as features.
    """
    ma_factor = SimpleMovingAverage(inputs = [USEquityPricing.close], window_length = 20)
    bb_factor = BollingerBands(inputs = [USEquityPricing.close], window_length = 20)
    ten_day_lookback_factor = TenDayLookbackPrice(inputs = [USEquityPricing.close], window_length = 10)
    return Pipeline(columns = {'moving_average' : ma_factor,
                               'bollinger_bands': bb_factor,
                               'ten_day_lookback' : ten_day_lookback_factor})

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
    new_column_labels = ['price_' + str(i) + '_back' for i in reversed(range(1,11))]
    # Transform the column with tuples to separate columns
    asset_df = tuples_to_columns(tuple_column_label = 'nday',
                                 new_column_labels = new_column_labels,
                                 df = pipeline_output('the_pipeline'))
    expected_to_grow = context.classifier.predict(asset_df.values)
    # Gather the ticker for all assets that are expected to grow
    assets_to_grow = asset_df.index.tolist()[[True if exp == 1 else False for exp in expected_to_grow]]
    context.longs = assets_to_grow[:5]
    
def handle_data(context, data):  
    """Zipline built-in. Function called every trading day (if daily)."""
    if context.first_day:
        arr = train_classifier(context, data)
        context.first_day = False
        expected_to_grow = order_assets(context, data)
    record(asset_price = data.current(context.asset, 'close'))
