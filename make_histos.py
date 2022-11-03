import argparse
import numpy as np
import matplotlib.pyplot as plt
import json
from datetime import datetime, timedelta


def get_meta_str(path, arr):
    with open(path + '/campaign_config.json', 'r') as f:
        campaign_config = json.load(f)
    elapsed_time_htc = get_elapsed_time(path)
    elapsed_time_sum = np.sum(arr)
    total_calls = campaign_config["n_jobs"]*campaign_config["n_calls"]
    return f'executable:\n{campaign_config["executable"]}\n' \
           f'total calls:\n{total_calls} \n' \
           f'n_jobs: {campaign_config["n_jobs"]} \n' \
           f'n_calls: {campaign_config["n_calls"]}\n' \
           f'dt (htc): {elapsed_time_htc}\n' \
           f'f [hz]: {round(total_calls / elapsed_time_htc.seconds)}\n' \

#           f'dt (sum): {timedelta(seconds=elapsed_time_sum)}\n'


def get_elapsed_time(path):
    with open(path + '/log.log', 'r') as f:
        for line in f:
            if not ' Job executing on host:' in line:
                continue
            begin = line.split(' Job executing on host:')[0]
            begin = begin.split(') ')[1]
            begin = datetime.strptime(begin, "%Y-%m-%d %H:%M:%S")
            break
        for line in reversed(list(f)):
            if not ' Job terminated.' in line:
                continue
            end = line.split(' Job terminated.')[0]
            end = end.split(') ')[1]
            end = datetime.strptime(end, "%Y-%m-%d %H:%M:%S")
            break
        return end - begin


def get_raw_arrays(path):
    run_times = np.load(path + '/run_times.npy')
    http_codes = np.load(path + '/http_codes.npy')
    if run_times.size != http_codes.size:
        print('Problem: different number of run times and http codes')
    return run_times, http_codes


def decorate_info_box(axis, arr):
    min_, max_ = np.min(arr), np.max(arr)
    mu, sig = np.mean(arr), np.std(arr)
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    textstr = '\n'.join((r'$min=%.4f$' % (min_, ),
                         r'$max=%.4f$' % (max_, ),
                         r'$\mu=%.4f$' % (mu, ),
                         r'$\sigma=%.4f$' % (sig, )))
    axis.text(0.4, 0.95, textstr, transform=axis.transAxes, fontsize=12,
              verticalalignment='top', bbox=props)


def main(args):
    run_times, http_codes = get_raw_arrays(args.input)
    fig, axs = plt.subplots(1, 2, sharey=True)
    fig.suptitle('Curl Performance Summary')
    axs[0].hist(run_times)
    axs[0].set_xlabel('response time [s]')
    decorate_info_box(axs[0], run_times)
    axs[1].hist(http_codes)
    axs[1].set_xlabel('http code')
    plt.figtext(0.82, 0.5, get_meta_str(args.input, run_times), fontsize=8)
    plt.subplots_adjust(right=0.8)
    plt.yscale('log')
    plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, default='output/latest', help='output folder')
    args = parser.parse_args()
    main(args)
