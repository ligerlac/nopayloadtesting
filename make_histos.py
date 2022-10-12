import argparse
from nopayloadtesting.plotter import Plotter


def main(args):
    plotter = Plotter(args.output)
    plotter.load_raw_results()
    plotter.plot_run_times()

    print(f'run_times = {plotter.run_times}')
    print(f'http_codes = {plotter.http_codes}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=str, default='output/latest', help='output folder') 
    parser.add_argument('--njobs', type=int, default=2, help='number of jobs') 
    parser.add_argument('--ncalls', type=int, default=2, help='number of calls to service by job')
    parser.add_argument('--executable', type=str, default='executables/curl_lino.sh', help='path to executable')
    args = parser.parse_args()
    main(args)
