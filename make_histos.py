import argparse
import numpy as np
import matplotlib.pyplot as plt
import json
from datetime import datetime, timedelta
from nopayloadtesting.plotter import Plotter
from nopayloadtesting.summariser import Summariser
import glob


def main(args):
    for f in glob.glob(args.folder):
#        summariser = Summariser(f)
#        summariser.extract_raw_results()
#        summariser.save_raw_results()
        
        plotter = Plotter(folder=f)
        plotter.make_summary_plot()

    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--folder', type=str, default='output/latest', help='folder with test evaluation data')
    args = parser.parse_args()
    main(args)
