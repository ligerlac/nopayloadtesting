import argparse
import numpy as np
import matplotlib.pyplot as plt
import json
from datetime import datetime, timedelta
from nopayloadtesting.plotter import Plotter
from nopayloadtesting.summariser import Summariser
import glob


def main(args):
    #patterns = ['frr', 'fll', 'fff']
    patterns = ['frr', 'fff']
    means, norm_means, n_iovs = {}, {}, {}
    for pat in patterns:
        means[pat] = []
        norm_means[pat] = []
        n_iovs[pat] = []
    plotters = []
    for f in glob.glob(f'{args.folder}/*/*'):
        if 'fll' in f:
            continue
        plotters.append(Plotter(folder=f))
        
    for plotter in plotters:
        n = plotter.campaign_config['db_size_dict']['n_iov_attached']
        print(f'plotter.folder = {plotter.folder}, n = {n}')
        m = plotter.curl_times.mean()
        k = np.mean(plotter.get_normalised_curl_times())
        n_iovs[plotter.campaign_config['access_pattern']].append(n)
        means[plotter.campaign_config['access_pattern']].append(m)
        norm_means[plotter.campaign_config['access_pattern']].append(k)

    # sort n_iovs and means according to n_iovs
    for pat in patterns:
        n_iovs[pat], means[pat], norm_means[pat] = zip(
            *sorted(zip(n_iovs[pat], means[pat], norm_means[pat]), key=lambda pair: pair[0]))

#    for pat in patterns:
#        plt.plot(n_iovs[pat], means[pat], marker='+', label=pat)
    plt.plot(n_iovs['fff'], means['fff'], marker='+', label='first')
    plt.plot(n_iovs['frr'], means['frr'], marker='+', label='early random')
    plt.xlabel('n iovs')
    plt.ylabel('mean curl time [ms]')
    plt.legend(title='IOV Access Pattern')
#    plt.show()
    plt.savefig(f'{args.folder}/curl_times_scaling_plot.png')

    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--folder', type=str, default='output/latest', help='folder with test evaluation data')
    args = parser.parse_args()
    main(args)
