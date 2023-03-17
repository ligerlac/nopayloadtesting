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
    n_pll_list = [1, 2, 5, 10]
    #n_pll_list = [1]
    mean_times, mean_freqs, n_iovs = {}, {}, {}
    for pat in pat_list:
        mean_times[pat] = {}
        mean_freqs[pat] = {}
        n_iovs[pat] = {}
        for n_pll in n_pll_list:
            mean_times[pat][n_pll] = []
            mean_freqs[pat][n_pll] = []
            n_iovs[pat][n_pll] = []

    for plotter in plotters:
        n_pll = plotter.campaign_config['n_pll']
        pat = plotter.campaign_config['pattern']
        mean_times[pat][n_pll].append(plotter.mean_time)
        mean_freqs[pat][n_pll].append(plotter.mean_freq)
        n_iovs[pat][n_pll].append(plotter.campaign_config['n_iov'])

    print(f'n_iovs =\n{n_iovs}')

    # sort n_iovs and means according to n_iovs
    for pat in pat_list:
        for n_pll in n_pll_list:
            n_iovs[pat][n_pll], mean_freqs[pat][n_pll], mean_times[pat][n_pll] =\
                zip(*sorted(zip(n_iovs[pat][n_pll], mean_freqs[pat][n_pll], mean_times[pat][n_pll]),
                            key=lambda trip: trip[0]))

    for pat in pat_list:
        for n_pll in n_pll_list:
            plt.plot(n_iovs[pat][n_pll], mean_times[pat][n_pll], marker='+', label=f'{n_pll} PLLs, {pat}')
    plt.xlabel('number of IOVs')
    plt.ylabel('mean response time [ms]')
    plt.legend(title='IOV Access Pattern')
    plt.title(f"title")
    plt.show()
    #plt.savefig(f'{args.folder}/mean_times_vs_n_iovs.png')

    plt.clf()
    for pat in pat_list:
        for n_pll in n_pll_list:
            plt.plot(n_iovs[pat][n_pll], mean_freqs[pat][n_pll], marker='+', label=f'{n_pll} PLLs, {pat}')
    plt.xlabel('number of IOVs')
    plt.ylabel('mean response frequency [Hz]')
    plt.legend(title='IOV Access Pattern')
    plt.title(f"title")
    plt.show()
    #plt.savefig(f'{args.folder}/mean_freqs_vs_n_iovs.png')

    for pat in pat_list:
        plt.clf()
        for n_pll in n_pll_list:
            plt.plot(n_iovs[pat][n_pll], mean_times[pat][n_pll], marker='+', label=n_pll)
        plt.xlabel('number of IOVs')
        plt.ylabel('mean response time [ms]')
        plt.ylim(ymin=0)
        plt.legend(title='Payload Lists', ncols=2)
        plt.title(f"50 threads, 50 calls, '{pat}' access pattern")
        #plt.show()
        plt.savefig(f'{args.folder}/mean_times_vs_n_iovs_{pat}.png')

    for pat in pat_list:
        plt.clf()
        for n_pll in n_pll_list:
            plt.plot(n_iovs[pat][n_pll], mean_freqs[pat][n_pll], marker='+', label=n_pll)
        plt.xlabel('number of IOVs')
        plt.ylabel('mean response frequency [Hz]')
        plt.ylim(ymin=0)
        plt.legend(title='Payload Lists', ncols=2)
        plt.title(f"50 threads, 50 calls, '{pat}' access pattern")
        #plt.show()
        plt.savefig(f'{args.folder}/mean_freqs_vs_n_iovs_{pat}.png')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--folder', type=str, default='output/latest', help='folder with test evaluation data')
    args = parser.parse_args()
    main(args)
