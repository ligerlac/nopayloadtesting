import argparse
import numpy as np
import matplotlib.pyplot as plt
import json
from datetime import datetime, timedelta
from nopayloadtesting.plotter import Plotter
from nopayloadtesting.summariser import Summariser
import glob


def main(args):
    random_means, constant_means = [], []
    random_n_iovs, constant_n_iovs = [], []
    plotters = []
    for f in glob.glob('output/for_2022-11-18/*/*'):
#    for f in glob.glob('output/my_instance/*/*/*'):
        plotters.append(Plotter(folder=f))
        
    for plotter in plotters:
        n = plotter.campaign_config['db_size_dict']['n_iov_attached']
        m = plotter.curl_times.mean()
        if plotter.campaign_config['access_pattern'] == 'ccc':
            constant_n_iovs.append(n)
            constant_means.append(m)
        else:
            random_n_iovs.append(n)
            random_means.append(m)
    # sort n_iovs and means according to n_iovs
    random_n_iovs, random_means = zip(*sorted(zip(random_n_iovs, random_means), key=lambda pair: pair[0]))
    constant_n_iovs, constant_means = zip(*sorted(zip(constant_n_iovs, constant_means), key=lambda pair: pair[0]))
    plt.plot(random_n_iovs, random_means, label='random access pattern')
    plt.plot(constant_n_iovs, constant_means, label='constant access pattern')
    plt.xlabel('n iovs')
    plt.ylabel('mean curl time [ms]')
    plt.legend()
    plt.show()
#    plt.savefig('output/scaling_plot.png')
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
#    parser.add_argument('--folder', type=str, default='output/latest', help='folder with test evaluation data')
    args = parser.parse_args()
    main(args)
