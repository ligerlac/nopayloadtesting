import argparse
import numpy as np
import matplotlib.pyplot as plt
import json
from datetime import datetime, timedelta
from nopayloadtesting.plotter import Plotter, MTPlotter
from nopayloadtesting.summariser import Summariser
import glob


def main(args):
    pat_list = ['first', 'random', 'last']
    mean_times, mean_freqs, max_freqs, n_iovs, n_threads = {}, {}, {}, {}, {}
    for pat in pat_list:
        mean_times[pat] = []
        mean_freqs[pat] = []
        max_freqs[pat] = []
        n_iovs[pat] = []
        n_threads[pat] = []
    plotters = []
    for f in glob.glob(f'{args.folder}/*/*'):
        print(f'f = {f}')
        plotters.append(MTPlotter(folder=f))
        
    for plotter in plotters:
        pat = plotter.campaign_config['pattern']
        mean_times[pat].append(plotter.mean_time)
        mean_freqs[pat].append(plotter.mean_freq)
        max_freqs[pat].append(plotter.max_freq)
        n_iovs[pat].append(plotter.campaign_config['n_iov'])
        n_threads[pat].append(plotter.campaign_config['n_threads'])

    # sort n_iovs and means according to n_pods
    for pat in pat_list:
        n_threads[pat], n_iovs[pat], max_freqs[pat], mean_freqs[pat], mean_times[pat] = zip(*sorted(zip(n_threads[pat], n_iovs[pat], max_freqs[pat], mean_freqs[pat], mean_times[pat]), key=lambda trip: trip[0]))

    print(n_threads['first'])
    print(max_freqs['first'])
    print(max_freqs['random'])
    print(max_freqs['last'])

    for pat in pat_list:
        plt.plot(n_threads[pat], mean_times[pat], marker='+', label=pat)
    plt.xlabel('number of threads')
    plt.ylabel('mean response time [ms]')
    #plt.xlim([0, 60])
    plt.legend(title='IOV Access Pattern')
    plt.title(f"DB filled with {n_iovs['random'][0]} IOVs")
    #plt.show()
    plt.savefig(f'{args.folder}/mean_times_vs_n_threads.png')

    plt.clf()
    for pat in pat_list:
        plt.plot(n_threads[pat], mean_freqs[pat], marker='+', label=pat)
    plt.xlabel('number of threads')
    plt.ylabel('mean response frequency [Hz]')
    plt.xlim([0, 60])
    plt.legend(title='IOV Access Pattern')
    plt.title(f"DB filled with {n_iovs['random'][0]} IOVs")
    #plt.show()
    plt.savefig(f'{args.folder}/mean_freqs_vs_n_threads_zoomed.png')

    plt.clf()
    for pat in pat_list:
        plt.plot(n_threads[pat], max_freqs[pat], marker='+', label=pat)
    plt.xlabel('number of threads')
    plt.ylabel('max request frequency [Hz]')
    #plt.xlim([0, 60])
    plt.legend(title='IOV Access Pattern')
    plt.title(f"DB filled with {n_iovs['random'][0]} IOVs")
   # plt.show()
    plt.savefig(f'{args.folder}/max_freqs_vs_n_threads.png')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--folder', type=str, default='output/latest', help='folder with test evaluation data')
    args = parser.parse_args()
    main(args)
