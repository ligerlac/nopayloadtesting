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
    random_norm_means, constant_norm_means = [], []
    random_n_iovs, constant_n_iovs = [], []
    random_n_pods, constant_n_pods = [], []
    plotters = []
    for f in glob.glob(f'{args.folder}/*/*/*'):
        print(f'f = {f}')
        plotters.append(Plotter(folder=f))
        
    for plotter in plotters:
        n = plotter.campaign_config['db_size_dict']['n_iov_attached']
        print(f'plotter.folder = {plotter.folder}, n = {n}')
        m = plotter.curl_times.mean()
        k = np.mean(plotter.get_normalised_curl_times())
        if plotter.campaign_config['access_pattern'] == 'ccc':
            constant_n_iovs.append(n)
            constant_means.append(m)
            constant_norm_means.append(k)
            constant_n_pods.append(int(plotter.folder.split('/')[-2]))
        else:
            random_n_iovs.append(n)
            random_means.append(m)
            random_norm_means.append(k)
            random_n_pods.append(int(plotter.folder.split('/')[-2]))
    # sort n_iovs and means according to n_pods
    print(f'random_n_pods = {random_n_pods}')
    print(f'random_means = {random_means}')
    random_n_pods, random_n_iovs, random_means, random_norm_means = zip(*sorted(zip(random_n_pods, random_n_iovs, random_means, random_norm_means), key=lambda pair: pair[0]))
    random_norm_means = random_norm_means / np.max(random_norm_means)
#    constant_n_pods, constant_n_iovs, constant_means, constant_norm_means = zip(*sorted(zip(constant_n_pods, constant_n_iovs, constant_means, constant_norm_means), key=lambda pair: pair[0]))
#    plt.plot(random_n_pods, random_means, marker='+', label='2M Payload IOVs')
    plt.plot(random_n_pods, random_norm_means, marker='+', label='2M Payload IOVs')
#    plt.plot(constant_n_pods, constant_means, marker='+', label='constant access pattern')
    plt.xlabel('number of pods')
    plt.xticks(range(1, 11))
    plt.ylabel('normalized response time')
    plt.legend()
    #plt.show()
    plt.savefig(f'{args.folder}/norm_curl_times_vs_n_pods.png')

#    plt.clf()
#    plt.plot(random_n_iovs, random_norm_means, marker='+', label='random access pattern')
#    plt.plot(constant_n_iovs, constant_norm_means, marker='+', label='constant access pattern')
#    plt.xlabel('n iovs')
#    plt.ylabel('curl time ratio (npdb / google)')
#    plt.legend()
#    plt.show()
#    plt.savefig(f'{args.folder}/norm_curl_times_scaling_plot.png')


    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--folder', type=str, default='output/latest', help='folder with test evaluation data')
    args = parser.parse_args()
    main(args)
