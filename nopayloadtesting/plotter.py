import numpy as np
import matplotlib.pyplot as plt
import json
from datetime import datetime, timedelta


class Plotter:
    def __init__(self, folder):
        self.folder = folder
        self.run_times = np.load(folder + '/run_times.npy')
        self.http_codes = np.load(folder + '/http_codes.npy')
        if self.run_times.size != self.http_codes.size:
            print('Problem: different number of run times and http codes')

    def get_meta_str(self):
        with open(self.folder + '/campaign_config.json', 'r') as f:
            campaign_config = json.load(f)
        elapsed_time_htc = self.get_elapsed_time()
        elapsed_time_sum = np.sum(self.run_times)
        total_calls = campaign_config["n_jobs"]*campaign_config["n_calls"]
        print(f'campaign_config = {campaign_config}')
        return f'client_conf:\n{campaign_config["client_conf"]}\n' \
               f'total calls:\n{total_calls} \n' \
               f'n_jobs: {campaign_config["n_jobs"]} \n' \
               f'n_calls: {campaign_config["n_calls"]}\n' \
               f'dt (htc): {elapsed_time_htc}\n' \
               f'avg. f [hz]: {round(total_calls / elapsed_time_htc.seconds)}\n' \
               f'acc. pattern: {campaign_config["access_pattern"]}\n' \
               f'n_global_tag: {campaign_config["db_size_dict"]["n_global_tag"]}\n' \
               f'n_iov_attached: {campaign_config["db_size_dict"]["n_iov_attached"]}\n' \
               f'n_iov_tot: {campaign_config["db_size_dict"]["n_iov_tot"]}\n' \
               

    def get_elapsed_time(self):
        with open(self.folder + '/log.log', 'r') as f:
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


    def make_summary_plot(self):
        fig, axs = plt.subplots(1, 2, sharey=True)
        fig.set_figheight(5)
        fig.set_figwidth(11)
        fig.suptitle('Curl Performance Summary')
        axs[0].hist(self.run_times)
        axs[0].set_xlabel('response time [s]')
        decorate_info_box(axs[0], self.run_times)
        axs[1].hist(self.http_codes)
        axs[1].set_xlabel('error code')
        plt.figtext(0.82, 0.3, self.get_meta_str(), fontsize=11)
        plt.subplots_adjust(right=0.8)
        plt.yscale('log')
        plt.savefig(f'{self.folder}/summary_plot.png')
#        plt.show()


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
