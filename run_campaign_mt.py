import requests
import shutil
import argparse
import numpy as np
import random
import sys
import json
import threading
from datetime import datetime
from pathlib import Path


def main(args):

    if not args.pattern in ["random", "first", "last"]:
        sys.exit(f"invalid pattern: '{args.pattern}'. chose from ['random', 'first', 'last']")

    base_url = f'http://{args.hostname}/api/cdb_rest'

    # get number of piovs in the db
    res = requests.get(base_url+'/globalTags')
    n_iov = res.json()[0]['payload_iov_count']
    n_pll = res.json()[0]['payload_lists_count']

    piov_url = base_url + '/' + args.endpoint + '/?gtName=global_tag_0&majorIOV={iov}&minorIOV=0'

    def get_piov_url():
        if args.pattern == 'first':
            iov = 0
        elif args.pattern == 'last':
            iov = n_iov
        else:
            iov = random.randint(0, n_iov)
        return piov_url.format(iov=iov)        


    def make_calls(n_calls, result_dict, dict_index):
        beg_ts, end_ts = [], []
        for i in range(n_calls):
            beg_ts.append(datetime.now().timestamp())
            res = requests.get(get_piov_url())
            end_ts.append(datetime.now().timestamp())
        result_dict[dict_index] = [beg_ts, end_ts]
        

    # Build the threads (results will be stored in ts_dict)
    ts_dict = {}
    threads = []
    for j in range(args.nthreads):
        t = threading.Thread(target=make_calls, args=(args.ncalls, ts_dict, j))
        threads.append(t)

    # Run the threads
    t_0 = datetime.now()
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print(f'conducted {args.ncalls*args.nthreads} calls in {datetime.now()-t_0}')

    # Extract correctly ordered arrays
    beg_ts, end_ts = [], []
    for x in ts_dict.values():
        beg_ts += x[0]
        end_ts += x[1]

    p = Path(Path.cwd() / args.output)
    shutil.rmtree(p, ignore_errors=True)
    p.mkdir(parents=True, exist_ok=True)

    np.save(args.output+'/curl_begins.npy', np.array(beg_ts))
    np.save(args.output+'/curl_ends.npy', np.array(end_ts))

    config_dict = {'pattern': args.pattern, 'n_calls': args.ncalls, 'n_threads': args.nthreads, 'n_iov': n_iov, 'n_pll': n_pll}
    with open(args.output + '/campaign_config.json', 'w') as f:
        json.dump(config_dict, f)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    date_str = datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")[:-3]
    parser.add_argument('--output', type=str, default=f'output/{date_str}', help='output folder') 
    parser.add_argument("--hostname", type=str, default="test111.apps.usatlas.bnl.gov")
    parser.add_argument("--ncalls", type=int, default=100, help="number of calls to service per thread")
    parser.add_argument("--nthreads", type=int, default=100)
    parser.add_argument("--pattern", type=str, default="random", help=["random", "first", "last"])
    parser.add_argument("--endpoint", type=str, default="payloadiovstest", help=["random", "first", "last"])
#    parser.add_argument("--insert", type=bool, default=false)
    args = parser.parse_args()
    main(args)
