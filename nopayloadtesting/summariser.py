import re, glob, os
import numpy as np
import time


class Summariser:
    def __init__(self, output):
        self.output = output
        self.curl_begins = None
        self.curl_ends = None
        self.client_begins = None
        self.client_ends = None
        self.http_codes = None
        self.test_curl_times = None
        self.job_ids = None
        self.failed_tests = None
        self.db_size_dict = None


    def extract_raw_results(self):
        _curl_begins, _curl_ends, _client_begins, _client_ends, _http_codes, _test_curl_times, _job_ids, _failed_tests = [], [], [], [], [], [], [], []
        for fn in glob.iglob(f'{self.output}/jobs/*out'):
            with open(fn, 'r') as f:
                for line in f:
                    if re.search('test curl took', line):
                        _job_ids.append(int(fn.split('/')[-1].split('.out')[0]))
                        _test_curl_times.append(float(line.split('test curl took ')[1].split(' ')[0]))
                    elif re.search('aborting...', line):
                        _failed_tests.append(int(fn.split('/')[-1].split('.out')[0]))
                    elif re.search('begin client', line):
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
        self.test_curl_times = _test_curl_times
        self.failed_tests = _failed_tests
        self.job_ids = _job_ids

    
    def save_raw_results(self):
        np.save(self.output+'/curl_begins.npy', self.curl_begins)
        np.save(self.output+'/curl_ends.npy', self.curl_ends)
        np.save(self.output+'/client_begins.npy', self.client_begins)
        np.save(self.output+'/client_ends.npy', self.client_ends)
        np.save(self.output+'/http_codes.npy', self.http_codes)
        np.save(self.output+'/test_curl_times.npy', self.test_curl_times)
        np.save(self.output+'/failed_tests.npy', self.failed_tests)
        np.save(self.output+'/job_ids.npy', self.job_ids)


    def clean_up(self):
        time.sleep(1)
#        os.rmdir(self.output + '/jobs/')



