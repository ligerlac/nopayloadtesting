import argparse
import numpy as np
import matplotlib.pyplot as plt
import json
from datetime import datetime, timedelta
from nopayloadtesting.plotter import Plotter
import glob


def main(args):
    for f in glob.glob(args.folder):
        plotter = Plotter(folder=f)
        plotter.make_summary_plot()

    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--folder', type=str, default='output/latest', help='folder with test evaluation data')
    args = parser.parse_args()
    main(args)
