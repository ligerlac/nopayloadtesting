import argparse
#import numpy as np
import matplotlib.pyplot as plt
import json
from datetime import datetime, timedelta
from nopayloadtesting.plotter import Plotter, MTPlotter
from nopayloadtesting.summariser import Summariser
import glob


def main(args):
    #pod_list = [1, 2, 3, 4, 5]
    pod_list = [1, 2, 3, 5, 7, 10]
    mean_times, mean_freqs, max_freqs, n_iovs, n_threads = {}, {}, {}, {}, {}
    for pod in pod_list:
        mean_times[pod] = []
        mean_freqs[pod] = []
        max_freqs[pod] = []
        n_iovs[pod] = []
        n_threads[pod] = []
    plotters = []
    for f in glob.glob(f'{args.folder}/*/*/*'):
        print(f'f = {f}')
        plotters.append(MTPlotter(folder=f))
        
    for plotter in plotters:
        pod = int(plotter.folder.split('/')[-3])
        if pod not in pod_list:
            continue
        mean_times[pod].append(plotter.mean_time)
        mean_freqs[pod].append(plotter.mean_freq)
        max_freqs[pod].append(plotter.max_freq)
        n_iovs[pod].append(plotter.campaign_config['n_iov'])
        n_threads[pod].append(plotter.campaign_config['n_threads'])

    # sort everything according to n_threads
    for pod in pod_list:
        n_threads[pod], n_iovs[pod], max_freqs[pod], mean_freqs[pod], mean_times[pod] = zip(*sorted(zip(n_threads[pod], n_iovs[pod], max_freqs[pod], mean_freqs[pod], mean_times[pod]), key=lambda trip: trip[0]))

    print(n_threads)

    plt.clf()
    for pod in pod_list:
        plt.plot(n_threads[pod], mean_freqs[pod], marker='+', label=pod)
    plt.xlabel('number of threads')
    plt.ylabel('mean response frequency [Hz]')
    plt.xlim([0, 110])
    plt.ylim([0, 290])
    plt.legend(title='Number of pods', ncol=2)
    plt.title(f"DB filled with {n_iovs[1][0]} IOVs, random access pattern")
    plt.show()
    #plt.savefig(f'{args.folder}/pod_scaling.png')

    #plt.clf()
    #for pod in pod_list:
    #    plt.plot(n_threads[pod], mean_freqs[pod], marker='+', label=pod)
    #plt.xlabel('number of threads')
    #plt.ylabel('mean response frequency [Hz]')
    ##plt.xlim([0, 110])
    #plt.xlim([0, 25])
    #plt.ylim([0, 200])
    #plt.legend(title='Number of pods', ncol=2)
    #plt.title(f"DB filled with {n_iovs[1][0]} IOVs, random access pattern")
    ##plt.show()
    #plt.savefig(f'{args.folder}/pod_scaling_zoomed.png')

    #plt.clf()
    #for pod in pod_list:
    #    norm_freq = mean_freqs[pod] / max(mean_freqs[pod])
    #    plt.plot(n_threads[pod], norm_freq, marker='+', label=pod)
    #plt.xlabel('number of threads')
    #plt.ylabel('normalised mean response frequency [a.u.]')
    #plt.xlim([0, 55])
    ##plt.xlim([0, 22])
    #plt.legend(title='Number of pods', ncol=2)
    #plt.title(f"DB filled with {n_iovs[1][0]} IOVs, random access pattern")
    #plt.show()
    #plt.savefig(f'{args.folder}/pod_scaling_norm.png')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--folder', type=str, default='output/latest', help='folder with test evaluation data')
    args = parser.parse_args()
    main(args)
