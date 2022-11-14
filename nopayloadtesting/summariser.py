import re, glob
import numpy as np


class Summariser:
    def __init__(self, output):
        self.output = output
        self.run_times = None
        self.curl_times = None
        self.http_codes = None
        self.db_size_dict = None

#requesting payload url for gt=global_tag_0, pt=pl_type_0, and iov=0
#res=Time difference = 1.53558[s] {"code":0,"msg":"/lbne/u/lgerlach1/Projects/nopayloadclient/data/remote/global_tag_0/pl_type_0/0_0.dat"}
#runtime=22.315281096

    def extract_raw_results(self):
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
        np.save(self.output+'/run_times.npy', self.run_times)
        np.save(self.output+'/curl_times.npy', self.curl_times)
        np.save(self.output+'/http_codes.npy', self.http_codes)

