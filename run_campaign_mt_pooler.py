import requests
import shutil
import argparse
import numpy as np
import random
import sys
import json
import threading
import concurrent.futures
from datetime import datetime
from pathlib import Path
from nopayloadtesting.constants import MAX_IOV


def main(args):
    base_url = f'http://{args.hostname}/api/cdb_rest'

    # get number of piovs in the db
#    res = requests.get(base_url + '/globalTags')
#    n_iov = res.json()[0]['payload_iov_count']
#    n_pll = res.json()[0]['payload_lists_count']
    n_iov = 1
    n_pll = 1

    piov_url = base_url + '/' + args.endpoint + '/?gtName=' + args.gt + \
               '&majorIOV={major}&minorIOV={minor}'

    print(f'piov_url = {piov_url}')

    def get_piov_url():
        if (args.major != -1) or (args.minor != -1):
            return piov_url.format(major=args.major, minor=args.minor)
        if args.pattern == 'first':
            major, minor = 0, 0
        elif args.pattern == 'last':
            major, minor = MAX_IOV, MAX_IOV
        else:
            major, minor = random.randint(0, MAX_IOV), random.randint(0, MAX_IOV)
        return piov_url.format(major=major, minor=minor)

    def make_call(url):
        beg_ts = datetime.now().timestamp()
        res = requests.get(url)
        # print(f'url = {url}')
        # print(res.json())
        return beg_ts, datetime.now().timestamp()

    urls = [get_piov_url() for _ in range(args.ncalls)]
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.nthreads) as executor:
        ts_pairs = executor.map(make_call, urls)

    # Extract correctly ordered arrays
    beg_ts, end_ts = [], []
    for x in list(ts_pairs):
        beg_ts.append(x[0])
        end_ts.append(x[1])

    p = Path(Path.cwd() / args.output)
    shutil.rmtree(p, ignore_errors=True)
    p.mkdir(parents=True, exist_ok=True)

    np.save(args.output + '/curl_begins.npy', np.array(beg_ts))
    np.save(args.output + '/curl_ends.npy', np.array(end_ts))

    config_dict = {'pattern': args.pattern, 'n_calls': args.ncalls, 'n_threads': args.nthreads, 'n_iov': n_iov,
                   'n_pll': n_pll}
    with open(args.output + '/campaign_config.json', 'w') as f:
        json.dump(config_dict, f)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    date_str = datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f')[:-3]
    parser.add_argument('--output', type=str, default=f'output/{date_str}', help='output folder')
    parser.add_argument('--hostname', type=str, default='test111.apps.usatlas.bnl.gov')
    parser.add_argument('--ncalls', type=int, default=100, help='number of calls to service per thread')
    parser.add_argument('--nthreads', type=int, default=100)
    parser.add_argument('--pattern', type=str, default='random', choices=['random', 'first', 'last'])
    parser.add_argument('--major', default=-1, type=int, help='overrides pattern')
    parser.add_argument('--minor', default=-1, type=int, help='overrides pattern')
    parser.add_argument('--endpoint', type=str, default='payloadiovstest', help=['random', 'first', 'last'])
    parser.add_argument('--gt', type=str, default='my_gt')
    #    parser.add_argument('--insert', type=bool, default=false)
    args = parser.parse_args()
    main(args)
