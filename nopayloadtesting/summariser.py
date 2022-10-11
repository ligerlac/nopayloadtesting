import re, glob, shutil
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt


class Summariser:
    def __init__(self, output):
        self.output = output
        self.run_times = None
        self.http_codes = None


    def extract_raw_results(self):
        _run_times, _http_codes = [], []
        for fn in glob.iglob(f'{self.output}/campaign/*out'):
            print(f'fn = {fn}')
            with open(fn, 'r') as f:
                for line in f:
                    if re.search('runtime', line):
                        _run_times.append(float(line.split('runtime=')[1].strip()))
                    if re.search('httpcode', line):
                        _http_codes.append(int(line.split('httpcode=')[1].strip()))
        self.run_times = np.array(_run_times)
        self.http_codes = np.array(_http_codes)

    
    def save_raw_results(self):
        np.save(self.output+'/run_times.npy', self.run_times)
        np.save(self.output+'/http_codes.npy', self.http_codes)

