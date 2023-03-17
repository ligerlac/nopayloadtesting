import numpy as np
import matplotlib.pyplot as plt
import json
from datetime import datetime, timedelta


class MTPlotter:
    def __init__(self, folder):
        self.folder = folder
        self.curl_begins = np.load(folder + '/curl_begins.npy')*1000
        self.curl_ends = np.load(folder + '/curl_ends.npy')*1000
        print(f'self.curl_begins.size = {self.curl_begins.size}')
        self.curl_times = self.curl_ends - self.curl_begins
        self.mean_time = self.curl_times.mean()
        self.std_time = np.std(self.curl_times)
        with open(self.folder + '/campaign_config.json', 'r') as f:
            self.campaign_config = json.load(f)
        self.dt_wc = self.curl_ends.max() - self.curl_begins.min()
        self.dt_sum = np.sum(self.curl_times)
        self.total_calls = self.curl_times.size
        self.mean_freq = self.total_calls / self.dt_wc * 1000
        self.max_freq = self.get_max_freq()

    def get_meta_str(self):
        cc = self.campaign_config
        print(f'cc = {cc}')
        return f'total calls:\n{self.total_calls} \n' \
               f'n_threads: {cc["n_threads"]} \n' \
               f'n_calls: {cc["n_calls"]}\n' \
               f'wall clock [s]: {round(self.dt_wc/1000, 1)}\n' \
               f'avg. f [hz]: {round(self.mean_freq, 1)}\n' \
               f'acc. pattern: {cc["pattern"]}\n' \
               f'n_pll: {cc["n_pll"]}\n' \
               f'n_iov:\n{cc["n_iov"]}\n'

    def make_compact_summary_plot(self):
        fig, axs = plt.subplots(1, 2)
        #        fig.set_figheight(10)
        #        fig.set_figwidth(11)
        fig.set_figheight(5)
        fig.set_figwidth(10)
        fig.suptitle('nopayloaddb Curl Performance Summary')

        axs[0].hist(self.curl_times)
        axs[0].set_xlabel('curl time [ms]')
        decorate_info_box(axs[0], self.curl_times)

        ts, n = self.get_ts_frequency()
        axs[1].plot(ts, n)
        axs[1].set_xlabel('elapsed time [s]')
        axs[1].set_ylabel('f [Hz]')

        plt.figtext(0.82, 0.3, self.get_meta_str(), fontsize=11)
        plt.subplots_adjust(right=0.8)
        #axs[0].set_yscale('log')
        #axs[1].set_yscale('log')

        plt.show()

    def get_max_freq(self):
        bin_middles, freqs = self.get_ts_frequency()
        return max(freqs)

    def get_ts_frequency(self):
        #request_time_stamps_sec = (self.curl_begins - self.curl_begins[0]) / 1000
        request_time_stamps_sec = (self.curl_ends - self.curl_begins[0]) / 1000
        duration = request_time_stamps_sec.max() - request_time_stamps_sec.min()
        n_bins = int(duration) + 1
        bins = list(range(n_bins + 1))
        frequency = np.histogram(request_time_stamps_sec, bins=bins)
        be = frequency[1]
        bin_middles = [(be[i] + be[i + 1]) / 2 for i in range(len(be) - 1)]
        return bin_middles, frequency[0]


class Plotter:
    def __init__(self, folder):
        self.folder = folder
        self.curl_begins = np.load(folder + '/curl_begins.npy')
        self.curl_ends = np.load(folder + '/curl_ends.npy')
        self.client_begins = np.load(folder + '/client_begins.npy')
        self.client_ends = np.load(folder + '/client_ends.npy')
        self.http_codes = np.load(folder + '/http_codes.npy')
        self.failed_tests = np.load(folder + '/failed_tests.npy')
        self.test_curl_times = np.load(folder + '/test_curl_times.npy')
        self.job_ids = np.load(folder + '/job_ids.npy')
        self.curl_times = self.curl_ends - self.curl_begins
        self.client_times = self.client_ends - self.client_begins
        if not (self.curl_begins.size == self.curl_ends.size == self.client_begins.size == self.client_ends.size == self.http_codes.size):
            print('Problem: different number of run times and http codes')
            
        with open(self.folder + '/campaign_config.json', 'r') as f:
            self.campaign_config = json.load(f)

        self.job_dict = self.get_id_dict_from_log()


    def get_meta_str(self):
        cc = self.campaign_config
        elapsed_time_htc = self.get_elapsed_time()
        elapsed_time_sum = np.sum(self.client_times)
        total_calls = self.client_times.size#cc["n_jobs"]*cc["n_calls"]
        print(f'cc = {cc}')
        return f'total calls:\n{total_calls} \n' \
               f'n_jobs: {cc["n_jobs"]} \n' \
               f'n_calls: {cc["n_calls"]}\n' \
               f'dt (htc): {elapsed_time_htc}\n' \
               f'avg. f [hz]: {round(total_calls / elapsed_time_htc.seconds)}\n' \
               f'acc. pattern: {cc["access_pattern"]}\n' \
               f'n_global_tag: {cc["db_size_dict"]["n_global_tag"]}\n' \
               f'n_pt: {cc["db_size_dict"]["n_pt"]}\n' \
               f'n_iov_attached:\n{cc["db_size_dict"]["n_iov_attached"]}\n' \
#               f'n_iov_tot: {cc["db_size_dict"]["n_iov_tot"]}\n' \
               

    def get_id_dict_from_log(self):
        # this returns a dict: {id_0: {begin: b_0, end: e_0}, id_1: ...}
        # sorted by begin time stamps
        id_dict = {}
        with open(self.folder + '/log.log', 'r') as f:
            for line in list(f):
                if 'Job executing' in line:
                    job_id = int(line.split('(')[1].split(')')[0].split('.')[1])
                    begin = line.split(' Job executing on host:')[0]
                    begin = begin.split(') ')[1]
                    begin = datetime.strptime(begin, "%Y-%m-%d %H:%M:%S").timestamp()
                    host = line.split('on host: <')[1].split(':')[0]
                    id_dict[job_id] = {'begin': begin, 'host': host}
                if 'Job terminated.' in line:
                    job_id = int(line.split('(')[1].split(')')[0].split('.')[1])
                    end = line.split(' Job terminated.')[0]
                    end = end.split(') ')[1]
                    end = datetime.strptime(end, "%Y-%m-%d %H:%M:%S").timestamp()
                    id_dict[job_id]['end'] = end
        self.remove_unfinished_jobs(id_dict)
        return id_dict



    def remove_unfinished_jobs(self, jobs_dict):
        r = dict(jobs_dict)
        for job_id, job in r.items():
            if not 'end' in job:
                del jobs_dict[job_id]


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


    def get_ts_frequency(self):
        request_time_stamps_sec = (self.client_begins - self.client_begins[0])/1000
        duration = request_time_stamps_sec.max() - request_time_stamps_sec.min()
        n_bins = int(duration) + 1
        bins = list(range(n_bins+1))
        frequency = np.histogram(request_time_stamps_sec, bins=bins)
        be = frequency[1]
        bin_middles = [(be[i] + be[i+1]) / 2 for i in range(len(be)-1)]
        return bin_middles, frequency[0]
            

    def get_host_duration(self):
        good_hosts, bad_hosts = [], []
        good_durations, bad_durations = [], []
        for job_id, job_dict in self.job_dict.items():
            if job_id in self.failed_tests:
                bad_hosts.append(job_dict["host"])
                bad_durations.append(job_dict['end'] - job_dict['begin'])
            else:
                good_hosts.append(job_dict["host"])
                good_durations.append(job_dict['end'] - job_dict['begin'])
        labels = [str(l) for l in np.unique(np.concatenate([good_hosts, bad_hosts]), return_inverse=True)[1]]
        good_labels = labels[:len(good_durations)]
        bad_labels = labels[:len(bad_durations)]
        return good_labels, bad_labels, good_durations, bad_durations


    def get_good_and_bad_test_curl_times(self):
        good_times, bad_times = [], []
        for i, job_id in enumerate(self.job_ids):
            if job_id in self.failed_tests:
                bad_times.append(self.test_curl_times[i])
            else:
                good_times.append(self.test_curl_times[i])
        return good_times, bad_times

    
    def get_normalised_curl_times(self):
        good_times = self.get_good_and_bad_test_curl_times()[0]
        normalised_curl_times = []
        n_calls = self.campaign_config['n_calls']
        for i, g_t in enumerate(good_times):
            normalised_curl_times = [*normalised_curl_times, *self.curl_times[i*n_calls:(i+1)*n_calls]/g_t/1000]
        return normalised_curl_times
#        good_test_curl_times = self.get_good_and_bad_test_curl_times()[0]
#        mean_test_curl_time = np.mean(good_test_curl_times)
#        return self.curl_times / mean_test_curl_time
    

    def make_summary_plot(self):
        fig, axs = plt.subplots(3, 3)
#        fig.set_figheight(10)
#        fig.set_figwidth(11)
        fig.set_figheight(10)
        fig.set_figwidth(10)
        fig.suptitle('nopayloaddb Curl Performance Summary')
        axs[0][0].hist(self.client_times)
        axs[0][0].set_xlabel('client time [ms]')
        decorate_info_box(axs[0][0], self.client_times)
        
        axs[0][1].hist(self.curl_times)
        axs[0][1].set_xlabel('curl time [ms]')
        decorate_info_box(axs[0][1], self.curl_times)
        
        normalised_curl_times = self.get_normalised_curl_times()
        axs[0][2].hist(normalised_curl_times)
        axs[0][2].set_xlabel('curl time ratio (npdb / google)')
        decorate_info_box(axs[0][2], normalised_curl_times)
        
        ts, n = self.get_ts_frequency()
        axs[1][0].plot(ts, n)
        axs[1][0].set_xlabel('elapsed time [s]')
        axs[1][0].set_ylabel('f [Hz]')
        
        good_labels, bad_labels, good_durations, bad_durations = self.get_host_duration()
        axs[1][1].scatter(good_labels, good_durations)
        axs[1][1].scatter(bad_labels, bad_durations)
        axs[1][1].set_xlabel('host node [a.u.]')
        axs[1][1].set_ylabel('job duration [s]')

        axs[1][2].hist(self.http_codes)
        axs[1][2].set_xlabel('error code')

        good_times, bad_times = self.get_good_and_bad_test_curl_times()
        axs[2][0].hist(good_times, bins=[0.5*i for i in range(21)])
        axs[2][0].hist(bad_times, bins=[0.5*i for i in range(21)])
        axs[2][0].set_xlabel('test curl time [s]')

        axs[2][1].hist(good_times)
        axs[2][1].set_xlabel('test curl time [s]')

        plt.figtext(0.82, 0.3, self.get_meta_str(), fontsize=11)
        plt.subplots_adjust(right=0.8)
        axs[0][0].set_yscale('log')
        axs[0][1].set_yscale('log')
        axs[0][2].set_yscale('log')

        plt.show()
#        plt.savefig(f'{self.folder}/summary_plot.png')
#        plt.savefig(f'output/{self.folder.replace("/", "-")}.png')


    def make_compact_summary_plot(self):
        fig, axs = plt.subplots(1, 2)
        #        fig.set_figheight(10)
        #        fig.set_figwidth(11)
        fig.set_figheight(5)
        fig.set_figwidth(10)
        fig.suptitle('nopayloaddb Curl Performance Summary')

        axs[0].hist(self.curl_times)
        axs[0].set_xlabel('curl time [ms]')
        decorate_info_box(axs[0], self.curl_times)

        ts, n = self.get_ts_frequency()
        axs[1].plot(ts, n)
        axs[1].set_xlabel('elapsed time [s]')
        axs[1].set_ylabel('f [Hz]')


        plt.figtext(0.82, 0.3, self.get_meta_str(), fontsize=11)
        plt.subplots_adjust(right=0.8)
        #axs[0].set_yscale('log')
        #axs[1].set_yscale('log')

        plt.show()
#        plt.savefig(f'{self.folder}/summary_plot.png')
#        plt.savefig(f'output/{self.folder.replace("/", "-")}.png')


def decorate_info_box(axis, arr):
    min_, max_ = np.min(arr), np.max(arr)
    mu, sig, md = np.mean(arr), np.std(arr), np.median(arr)
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    textstr = '\n'.join((r'$min=%.1f$' % (min_, ),
                         r'$max=%.1f$' % (max_, ),
                         r'$\mu=%.1f$' % (mu, ),
                         r'$\sigma=%.1f$' % (sig, ),
                         r'$med=%.1f$' % (md, )))
    axis.text(0.6, 0.95, textstr, transform=axis.transAxes, fontsize=12,
              verticalalignment='top', bbox=props)
