import argparse
import numpy as np
import matplotlib.pyplot as plt
import json


def get_plot_title():
    with open(args.input + '/campaign_config.json', 'r') as f:
        campaign_config = json.load(f)
    return f'Curl Performance Summary\n' \
           f'n_jobs = {campaign_config["n_jobs"]}, n_calls = {campaign_config["n_calls"]}\n' \
           #f'executable =  {campaign_config["executable"]}'


def decorate_info_box(axis, arr):
    min_, max_ = np.min(arr), np.max(arr)
    mu, sig = np.mean(arr), np.std(arr)
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    textstr = '\n'.join((r'$min=%.2f$' % (min_, ),
                         r'$max=%.2f$' % (max_, ),
                         r'$\mu=%.2f$' % (mu, ),
                         r'$\sigma=%.2f$' % (sig, )))
    axis.text(0.4, 0.95, textstr, transform=axis.transAxes, fontsize=14,
              verticalalignment='top', bbox=props)


def main(args):
    run_times = np.load(args.input + '/run_times.npy')
    http_codes = np.load(args.input + '/http_codes.npy')

    if run_times.size != http_codes.size:
        print('Problem: different number of run times and http codes')

    fig, axs = plt.subplots(1, 2, sharey=True)
    fig.suptitle(get_plot_title())
    axs[0].hist(run_times)
    axs[0].set_xlabel('response time [s]')
    decorate_info_box(axs[0], run_times)
    axs[1].hist(http_codes)
    axs[1].set_xlabel('http code')
    plt.yscale('log')
    plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, default='output/latest', help='output folder')
    args = parser.parse_args()
    main(args)
