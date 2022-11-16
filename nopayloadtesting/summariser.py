import re, glob
import numpy as np


class Summariser:
    def __init__(self, output):
        self.output = output
        self.curl_begins = None
        self.curl_ends = None
        self.client_begins = None
        self.client_ends = None
        self.http_codes = None
        self.db_size_dict = None


    def extract_raw_results(self):
        _curl_begins, _curl_ends, _client_begins, _client_ends, _http_codes = [], [], [], [], []
        for fn in glob.iglob(f'{self.output}/jobs/*out'):
            with open(fn, 'r') as f:
                for line in f:
                    if re.search('begin client', line):
                        _client_begins.append(int(line.split('begin client: ')[1].strip()))
                    elif re.search('end client', line):
                        _client_ends.append(int(line.split('end client: ')[1].strip()))
                    elif re.search('res=', line):
                        _curl_begins.append(int(line.split('begin curl: ')[1].split(' ')[0]))
                        _curl_ends.append(int(line.split('end curl: ')[1].split(' ')[0]))
                        _http_codes.append(int(line.split('"code":')[1].split(',')[0].strip()))
        self.curl_begins = _curl_begins
        self.curl_ends = _curl_ends
        self.client_begins = _client_begins
        self.client_ends = _client_ends
        self.http_codes = _http_codes


    def extract_raw_results_old(self):
        _run_times, _curl_times, _http_codes = [], [], []
        for fn in glob.iglob(f'{self.output}/jobs/*out'):
            with open(fn, 'r') as f:
                for line in f:
                    if re.search('runtime', line):
                        _run_times.append(float(line.split('runtime=')[1].strip()))
                    elif re.search('"code":', line):
                        _http_codes.append(int(line.split('"code":')[1].split(',')[0].strip()))
                        _curl_times.append(float(line.split('Time difference = ')[1].split('[s]')[0]))
                    elif re.search('"code":', line):
                        _http_codes.append(int(line.split('"code":')[1].split(',')[0].strip()))
        self.run_times = np.array(_run_times)
        self.curl_times = np.array(_curl_times)
        self.http_codes = np.array(_http_codes)

    
    def save_raw_results(self):
        np.save(self.output+'/curl_begins.npy', self.curl_begins)
        np.save(self.output+'/curl_ends.npy', self.curl_ends)
        np.save(self.output+'/client_begins.npy', self.client_begins)
        np.save(self.output+'/client_ends.npy', self.client_ends)
        np.save(self.output+'/http_codes.npy', self.http_codes)


    def clean_up(self):
        os.rmdir(self.output + '/jobs/')



