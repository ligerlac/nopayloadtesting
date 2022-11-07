import argparse
import numpy as np
import matplotlib.pyplot as plt
import json
from datetime import datetime, timedelta
from nopayloadtesting.plotter import Plotter


def main(args):
    plotter = Plotter(folder=args.input)
    plotter.make_summary_plot()

    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, default='output/latest', help='folder with test evaluation data')
    args = parser.parse_args()
    main(args)
