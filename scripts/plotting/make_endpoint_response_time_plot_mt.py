import argparse
import numpy as np
import matplotlib.pyplot as plt
import json
from datetime import datetime, timedelta
from nopayloadtesting.plotter import Plotter, MTPlotter
from nopayloadtesting.summariser import Summariser
import glob


def main(args):

    plotters = []
    for f in glob.glob(f'{args.folder}/*/*'):
        print(f'f = {f}')
        plotters.append(MTPlotter(folder=f))

    #endpoint_list = ['payloadiovs', 'payloadiovs2', 'payloadiovsfast', 'payloadiovstest']
    endpoint_list = ['payloadiovs', 'payloadiovstest', 'payloadiovssql']
    #endpoint_list = ['payloadiovs', 'payloadiovsfast']
    #scenario_list = ['429496729', '858993458', '1288490188', '1717986918', '2147483647']#, 'worst-case']
    scenario_list = ['1000', '2000', '3000', '4000', '5000']#, 'worst-case']
    #scenario_list = ['tiny', 'tiny-moderate', 'moderate', 'heavy-usage']#, 'worst-case']
    mean_times, std_times, mean_freqs, std_freqs, n_iovs = {}, {}, {}, {}, {}
    for ep in endpoint_list:
        mean_times[ep] = {}
        std_times[ep] = {}
        mean_freqs[ep] = {}
        std_freqs[ep] = {}
        n_iovs[ep] = {}
        for scenario in scenario_list:
            mean_times[ep][scenario] = []
            std_times[ep][scenario] = []
            mean_freqs[ep][scenario] = []
            std_freqs[ep][scenario] = []
            n_iovs[ep][scenario] = []

    for plotter in plotters:
        scenario = plotter.folder.split('/')[-2]
        endpoint = plotter.folder.split('/')[-1]
        print(f'scenario = {scenario}, endpoint = {endpoint}')
        print(f'plotter.mean_time = {plotter.mean_time}')
        mean_times[endpoint][scenario].append(plotter.mean_time)
        std_times[endpoint][scenario].append(plotter.std_time)
        n_iovs[endpoint][scenario].append(plotter.campaign_config['n_iov'])

    #print(f'n_iovs =\n{n_iovs}')

    # sort n_iovs and means according to n_iovs
#    for ep in endpoint_list:
#        for scenario in scenario_list:
#            n_iovs[ep][scenario], std_freqs[ep][scenario], mean_freqs[ep][scenario], std_times[ep][scenario], mean_times[ep][scenario] =\
#                zip(*sorted(zip(n_iovs[ep][scenario], std_freqs[ep][scenario], mean_freqs[ep][scenario], std_times[ep][scenario], mean_times[ep][scenario]),
#                            key=lambda trip: trip[0]))

#    mapping = {'429496729': 1000, '858993458': 2000, '1288490188':3000,
#               '1717986918': 4000, '2147483647': 5000}#, 'worst-case']

    plt.clf()
    for ep in endpoint_list:
        xs, ys, es = [], [], []
        for scenario in scenario_list:
            if not mean_times[ep][scenario]:
                continue
            #xs.append(mapping[scenario])
            xs.append(scenario)
            ys.append(mean_times[ep][scenario][0])
            es.append(std_times[ep][scenario][0])
            #print(f'xs = {xs}')
            #print(f'ys = {ys}')
            #print(f'es = {es}')
        #plt.plot(xs, ys, marker='+', label=ep)
        plt.errorbar(xs, ys, es, marker='+', label=ep)
    plt.xlabel('IOVs per Payload List')
    plt.ylabel('mean response time [ms]')
    #plt.yscale('log')
    #plt.ylim([1, 350])
    plt.legend(title='endpoint')
    plt.title(f"1 thread, 50 calls")
    #plt.show()
    #plt.savefig(f'{args.folder}/endpoint_response_times.png')

    """
    plt.clf()
    for ep in ep_list:
        xs, ys = [], []
        for scenario in scenario_list:
            xs.append(scenario)
            ys.append(mean_times[ep][scenario])
        plt.plot(xs, ys, marker='+', label=ep)
    plt.xlabel('DB occupancy scenario')
    plt.ylabel('mean response time [ms]')
    #plt.ylim([0, 300])
    #plt.yscale('log')
    plt.legend(title='IOV Access eptern')
    plt.title(f"50 threads, 50 calls")
    #plt.show()
    #plt.savefig(f'{args.folder}/mean_times_vs_scenario.png')
    """

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--folder', type=str, default='output/latest', help='folder with test evaluation data')
    args = parser.parse_args()
    main(args)
