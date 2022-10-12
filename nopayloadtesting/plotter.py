import numpy as np
import matplotlib.pyplot as plt


class Plotter:
    def __init__(self, input):
        self.output = output
        self.run_times = None
        self.http_codes = None


    def load_raw_results(self):
        self.run_times = np.load(self.output + '/run_times.npy')
        self.http_codes = np.load(self.output + '/http_codes.npy')
        if self.run_times.size != self.http_codes.size:
            print('Problem: run_times and http_codes have different length')

    
    def plot_run_times(self):
        plt.hist(self.run_times)
        plt.show()
