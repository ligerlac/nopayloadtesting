import numpy as np
import matplotlib.pyplot as plt
import json
from datetime import datetime, timedelta


class Plotter:
    def __init__(self, folder):
        self.folder = folder
        self.curl_begins = np.load(folder + '/curl_begins.npy')
        self.curl_ends = np.load(folder + '/curl_ends.npy')
        self.client_begins = np.load(folder + '/client_begins.npy')
        self.client_ends = np.load(folder + '/client_ends.npy')
        self.http_codes = np.load(folder + '/http_codes.npy')
        self.curl_times = self.curl_ends - self.curl_begins
        self.client_times = self.client_ends - self.client_begins
        if not (self.curl_begins.size == self.curl_ends.size == self.client_begins.size == self.client_ends.size == self.http_codes.size):
            print('Problem: different number of run times and http codes')
        with open(self.folder + '/campaign_config.json', 'r') as f:
            self.campaign_config = json.load(f)


    def get_meta_str(self):
        cc = self.campaign_config
        elapsed_time_htc = self.get_elapsed_time()
        elapsed_time_sum = np.sum(self.client_times)
        total_calls = cc["n_jobs"]*cc["n_calls"]
        print(f'cc = {cc}')
        return f'client_conf:\n{cc["client_conf"]}\n' \
               f'total calls:\n{total_calls} \n' \
               f'n_jobs: {cc["n_jobs"]} \n' \
               f'n_calls: {cc["n_calls"]}\n' \
               f'dt (htc): {elapsed_time_htc}\n' \
               f'avg. f [hz]: {round(total_calls / elapsed_time_htc.seconds)}\n' \
               f'acc. pattern: {cc["access_pattern"]}\n' \
               f'n_global_tag: {cc["db_size_dict"]["n_global_tag"]}\n' \
               f'n_pt: {cc["db_size_dict"]["n_pt"]}\n' \
               f'n_iov_attached: {cc["db_size_dict"]["n_iov_attached"]}\n' \
               f'n_iov_tot: {cc["db_size_dict"]["n_iov_tot"]}\n' \
               

    def get_job_start_times(self):
        start_times = []
        with open(self.folder + '/log.log', 'r') as f:
            for line in f:
                if not ' Job executing on host:' in line:
                    continue
                begin = line.split(' Job executing on host:')[0]
                begin = begin.split(') ')[1]
                begin = datetime.strptime(begin, "%Y-%m-%d %H:%M:%S")        
                start_times.append(begin)
        return start_times

    
    def get_job_end_times(self):
        end_times = []
        with open(self.folder + '/log.log', 'r') as f:
            for line in list(f):
                if not ' Job terminated.' in line:
                    continue
                end = line.split(' Job terminated.')[0]
                end = end.split(') ')[1]
                end = datetime.strptime(end, "%Y-%m-%d %H:%M:%S")
                end_times.append(end)
        return end_times


    def get_id_dict_from_log(self):
        # this returns a dict: {id_0: {begin: b_0, end: e_0}, id_1: ...}
        # sorted by begin time stamps
        id_dict = {}
        with open(self.folder + '/log.log', 'r') as f:
            for line in list(f):
                if 'Job executing' in line:
                    job_id = line.split('(')[1].split(')')[0]
                    begin = line.split(' Job executing on host:')[0]
                    begin = begin.split(') ')[1]
                    begin = datetime.strptime(begin, "%Y-%m-%d %H:%M:%S").timestamp()
                    id_dict[job_id] = {'begin': begin}
                if 'Job terminated.' in line:
                    job_id = line.split('(')[1].split(')')[0]
                    end = line.split(' Job terminated.')[0]
                    end = end.split(') ')[1]
                    end = datetime.strptime(end, "%Y-%m-%d %H:%M:%S").timestamp()
                    id_dict[job_id]['end'] = end
        self.remove_unfinished_jobs(id_dict)
        return id_dict


    def get_jobs(self):
        # returns a list [{id: id_0, start: ...}, {...}]
        jobs = []
        id_dict = self.get_id_dict_from_log()
        job_ids = []
        start_time_stamps = []
        end_time_stamps = []
        for job_id, job in id_dict.items():
            job_ids.append(job_id)
            start_time_stamps.append(job['begin'])
            end_time_stamps.append(job['end'])
        for j, s, e in sorted(zip(job_ids, start_time_stamps, end_time_stamps), key=lambda triplet: triplet[2]):
            d = e - s
            f = self.campaign_config['n_calls'] / d
            jobs.append({'id': j, 'start': s, 'end': e, 'duration': d, 'freq': f})
        return jobs
            

    def remove_unfinished_jobs(self, jobs_dict):
        r = dict(jobs_dict)
        for job_id, job in r.items():
            try:
                _ = job['end']
            except KeyError:
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
        jobs = self.get_jobs()
        end_time_stamps = []
        frequencies = []
        for job in jobs:
            end_time_stamps.append(job['end'])
        for ts in end_time_stamps:
            f = 0
            for j in jobs:
                if j['start'] < ts <= j['end']:
                    f += j['freq']
            frequencies.append(f)
        return end_time_stamps, frequencies

            
    def get_ts_running_jobs(self):
        jobs = self.get_jobs()
        end_time_stamps = []
        running_jobs = []
        for job in jobs:
            end_time_stamps.append(job['end'])
        for ts in end_time_stamps:
            f = 0
            n = 0
            for j in jobs:
                if j['start'] < ts <= j['end']:
                    n += 1
            running_jobs.append(n)
        return end_time_stamps, running_jobs


    def make_summary_plot(self):
#        fig, axs = plt.subplots(2, 2, sharey='row')
        fig, axs = plt.subplots(2, 2)
        fig.set_figheight(7)
        fig.set_figwidth(11)
        fig.suptitle('Curl Performance Summary')
        axs[0][0].hist(self.client_times)
        axs[0][0].set_xlabel('response time [s]')
        decorate_info_box(axs[0][0], self.client_times)
        axs[0][1].hist(self.curl_times)
        axs[0][1].set_xlabel('curl time [s]')
        decorate_info_box(axs[0][1], self.curl_times)
        axs[1][0].hist(self.http_codes)
        axs[1][0].set_xlabel('error code')
        
        ts, n = self.get_ts_frequency()
        print(f'f = {n}')
        ts, n = self.get_ts_running_jobs()
        print(f'n = {n}')
        axs[1][1].plot(ts, n)
        axs[1][1].set_xlabel('elapsed time [s]')
        axs[1][1].set_ylabel('avg. f [Hz]')
        plt.figtext(0.82, 0.3, self.get_meta_str(), fontsize=11)
        plt.subplots_adjust(right=0.8)
        axs[0][0].set_yscale('log')
        axs[0][1].set_yscale('log')
#        plt.savefig(f'{self.folder}/summary_plot.png')
        plt.show()


def decorate_info_box(axis, arr):
    min_, max_ = np.min(arr), np.max(arr)
    mu, sig, md = np.mean(arr), np.std(arr), np.median(arr)
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    textstr = '\n'.join((r'$min=%.4f$' % (min_, ),
                         r'$max=%.4f$' % (max_, ),
                         r'$\mu=%.4f$' % (mu, ),
                         r'$\sigma=%.4f$' % (sig, ),
                         r'$median=%.4f$' % (md, )))
    axis.text(0.4, 0.95, textstr, transform=axis.transAxes, fontsize=12,
              verticalalignment='top', bbox=props)
