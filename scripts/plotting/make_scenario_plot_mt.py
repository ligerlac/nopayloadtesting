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

    pat_list = ['first', 'random', 'last']
    scenario_list = ['tiny', 'tiny-moderate', 'moderate', 'heavy-usage']#, 'worst-case']
    #scenario_list = ['moderate', 'heavy-usage', 'worst-case']
    #n_pll_list = [1]
    mean_times, mean_freqs, n_iovs = {}, {}, {}
    for pat in pat_list:
        mean_times[pat] = {}
        mean_freqs[pat] = {}
        n_iovs[pat] = {}
        for scenario in scenario_list:
            mean_times[pat][scenario] = []
            mean_freqs[pat][scenario] = []
            n_iovs[pat][scenario] = []

    for plotter in plotters:
        scenario = plotter.folder.split('/')[-2]
        if not scenario in scenario_list:
            continue
        print(f'scenario = {scenario}')
        pat = plotter.campaign_config['pattern']
        mean_times[pat][scenario].append(plotter.mean_time)
        mean_freqs[pat][scenario].append(plotter.mean_freq)
        n_iovs[pat][scenario].append(plotter.campaign_config['n_iov'])

    print(f'n_iovs =\n{n_iovs}')

    # sort n_iovs and means according to n_iovs
    for pat in pat_list:
        for scenario in scenario_list:
            n_iovs[pat][scenario], mean_freqs[pat][scenario], mean_times[pat][scenario] =\
                zip(*sorted(zip(n_iovs[pat][scenario], mean_freqs[pat][scenario], mean_times[pat][scenario]),
                            key=lambda trip: trip[0]))

    plt.clf()
    for pat in pat_list:
        xs, ys = [], []
        for scenario in scenario_list:
            xs.append(scenario)
            ys.append(mean_freqs[pat][scenario])
        plt.plot(xs, ys, marker='+', label=pat)
    plt.xlabel('DB occupancy scenario')
    plt.ylabel('mean response frequency [Hz]')
    plt.yscale('log')
    plt.ylim([1, 350])
    plt.legend(title='IOV Access Pattern')
    plt.title(f"50 threads, 50 calls")
    #plt.show()
    plt.savefig(f'{args.folder}/mean_freqs_vs_scenario.png')

    """
    plt.clf()
    for pat in pat_list:
        xs, ys = [], []
        for scenario in scenario_list:
            xs.append(scenario)
            ys.append(mean_times[pat][scenario])
        plt.plot(xs, ys, marker='+', label=pat)
    plt.xlabel('DB occupancy scenario')
    plt.ylabel('mean response time [ms]')
    #plt.ylim([0, 300])
    #plt.yscale('log')
    plt.legend(title='IOV Access Pattern')
    plt.title(f"50 threads, 50 calls")
    #plt.show()
    #plt.savefig(f'{args.folder}/mean_times_vs_scenario.png')
    """

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--folder', type=str, default='output/latest', help='folder with test evaluation data')
    args = parser.parse_args()
    main(args)
