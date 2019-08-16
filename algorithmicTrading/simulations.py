import pandas as pd
import os
import matplotlib.pyplot as plt
    
def readSimulation(simulation_file_name = 'ma_crossover_strategy.pickle',
                   simulation_file_dir = '../../simulations/',
                   subset_boundaries = None):
    '''
    readSimulation

    Function to read simulation, and instanstiate simulation class for file.
    '''
    # Read pickled simulation
    if not simulation_file_dir[-1] == '/':
        simulation_file_dir = simulation_file_dir + '/'
    try:
        full_simulation_dir = simulation_file_dir + simulation_file_name
        simulation = pd.read_pickle(simulation_file_dir + simulation_file_name)
    except TypeError:
        raise Exception('Simulation_file_dir and simulation_file_name must be strings')
    simulation = pd.read_pickle(full_simulation_dir)    
    if subset_boundaries is not None:
        if isinstance(subset_boundaries, list):
            simulation = simulation.loc[subset_boundaries[0]:subset_boundaries[1]]
    # Create Simulation instance
    simulation = Simulation(simulation_df = simulation)

    return simulation

class Simulation:
    '''
    Simulation

    Simulation class.
    '''
    def __init__(self, simulation_df):
        self.simulation_df = simulation_df

    def plotter(self, *args, show_plot = True, plot_transactions = False):
        '''
        plotter

        Method to plot simulation_df
        '''
        fig, ax = plt.subplots()
        for arg in args:
            plt.plot_date(y = self.simulation_df[arg],
                          x = self.simulation_df.index.values,
                          fmt = '-')
            fig.autofmt_xdate()
        if plot_transactions:
            # Subset based on where transactions happen, else empty list
            trans_subset = self.simulation_df[[trans != [] for trans in self.simulation_df['transactions']]]
            pos_dts, neg_dts = [], []
            # Get longs and closes
            for trans in trans_subset['transactions']:
                trans = trans[0] 
                if trans['amount'] > 0:
                    pos_dts.append(trans['dt'])
                else:
                    neg_dts.append(trans['dt'])
            pos_subset = trans_subset[trans_subset.index.isin(pos_dts)]
            neg_subset = trans_subset[trans_subset.index.isin(neg_dts)]
            
            for subset, c in zip((pos_subset, neg_subset), ('g', 'r')):
                plt.scatter(x = subset.index, y = subset['asset_price'], marker = 'x', c = c)
                
        if show_plot: plt.show()
        
        return plt
