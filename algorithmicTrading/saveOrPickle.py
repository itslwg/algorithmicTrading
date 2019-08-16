import json
import time
import pickle

def saveData(ticker, data_dict, 
             data_folder = '../../data/stock_data/'):
    """ This function saves or replaces current dict in disk to disk.
    :param ticker: The stock ticker. To be used in file_name.
    :type ticker: string.
    :param url: The data dictionary
    :type name: dictionary.
    """
    with open(data_folder + ticker + '_' + time.strftime("%d%m%Y") + '.json', 'w') as outfile:
        json.dump(data_dict, outfile)
        print ('Data for ' + ticker + ' saved to disk.')
    
def pickleStockInstance(ticker, stock_class_instance,
                        stock_instance_dir = '../../Stock_instances/'):
    """ This function cPickles the input class_instance
    :param ticker: The stock ticker. To be used as file_name with the current date
    :type ticker: string.
    :param stock_class_instance: The class instance to be pickled.
    :type stock_class_instance: class. 
    :param file_name: The file_name used when pickled to disk.
    :type file_name: string.
    """
    with open(stock_instance_dir + ticker + '_' + time.strftime('%d%m%Y'), 'wb') as outfile:
        # Instance Stock class
        class_instance = stock_class_instance
        # Dump
        pickle.dump(class_instance, outfile)
        # Verbose
        print ('Stock class instance of ' + ticker + ' dumped to disk.')
