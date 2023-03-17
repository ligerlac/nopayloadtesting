import argparse
import logging
from nopayloadtesting.simpleclient import SimpleClient
from nopayloadtesting.constants import MAX_IOV
import sys
import random


def get_random_piov_list(pll_name, n_iovs):
    piov_list = []
    for i in range(n_iovs):
        major = random.randint(0, MAX_IOV)
        minor = random.randint(0, MAX_IOV)
        piov = {
            'payload_url': f'{pll_name}_{major}_{minor}_file.data',
            'payload_list': pll_name,
            'major_iov': major,
            'minor_iov': minor
        }
        piov_list.append(piov)
    return piov_list


def main(args):

    logging.basicConfig(level=args.loglevel.upper())

    client = SimpleClient(f'http://{args.hostname}/api/cdb_rest/')

    client.create_global_tag('my_gt')

    for i in range(args.n_pt):
        client.create_payload_type(f'my_pt_{i}')
        pll_name = client.get_payload_list_name('my_gt', f'my_pt_{i}')
        piov_list = get_random_piov_list(pll_name, args.n_iov)
        client.insert_payload_iov_list(piov_list)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--hostname', type=str, default='localhost:8000')
    parser.add_argument('--loglevel', choices=['warning', 'info', 'debug'], default='warning')
    parser.add_argument('--n_pt', type=int, default=1)
    parser.add_argument('--n_iov', type=int, default=1)
    args = parser.parse_args()
    main(args)
