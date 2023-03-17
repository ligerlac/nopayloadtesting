import argparse
#import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import json
from datetime import datetime, timedelta
from nopayloadtesting.plotter import Plotter, MTPlotter
from nopayloadtesting.summariser import Summariser
import glob


def main(args):
    #pod_list = [1, 2, 3, 4, 5]
    pod_list = range(1, 26)
    mean_times, mean_freqs, std_freqs = {}, {}, {}
    for pod in pod_list:
        mean_times[pod] = []
        mean_freqs[pod] = []
        std_freqs[pod] = []
    plotters = []
    for f in glob.glob(f'{args.folder}/*'):
        plotters.append(MTPlotter(folder=f))
        
    for plotter in plotters:
        print(plotter.campaign_config)
        pod = int(plotter.folder.split('/')[-1])
        if not pod in pod_list:
            continue
        _, freqs = plotter.get_ts_frequency()
        mean_times[pod].append(plotter.mean_time)
        mean_freqs[pod].append(plotter.mean_freq)
        #std_freqs[pod].append(np.std(freqs))
        e = mean_freqs[pod][0] / np.sqrt(plotter.total_calls)
        std_freqs[pod].append(e)

    plt.clf()
    xs, ys, es = [], [], []
    for pod in pod_list:
        xs.append(pod)
        ys.append(mean_freqs[pod][0])
        es.append(std_freqs[pod][0])
    coef = np.polyfit(xs, ys, 1)
    print(f'coef = {coef}')
    poly1d_fn = np.poly1d(coef)

    plt.errorbar(xs, ys, es, marker='+', label=pod)
    plt.plot(xs, poly1d_fn(xs), marker='', label=pod)
    plt.xlabel('number of pods')
    plt.ylabel('mean response frequency [Hz]')
    plt.ylim(ymin=0)
    #plt.xlim([0, 110])
    #plt.ylim([0, 290])
    #plt.legend(title='Number of pods', ncol=2)
    plt.title(f"'moderate' scenario, 'payloadiovstest' endpoint, 'random' iov pattern")
    #plt.show()
    plt.savefig(f'{args.folder}/single_pod_scaling.png')

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
