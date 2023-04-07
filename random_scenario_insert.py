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

    if args.scenario == 'tiny':
        args.n_pt = 10
        args.n_iov = 10
    elif args.scenario == 'tiny-moderate':
        args.n_pt = 10
        args.n_iov = 200
    elif args.scenario == 'moderate':
        args.n_pt = 100
        args.n_iov = 200
    elif args.scenario == 'heavy-usage':
        args.n_pt = 100
        args.n_iov = 5000
    elif args.scenario == 'worst-case':
        args.n_pt = 200
        args.n_iov = 26000
    else:
        sys.exit(f"invalid scenario: '{args.scenario}'. chose from ['tiny', 'tiny-moderate', 'moderate', 'heavy-usage', 'worst-case']")


    logging.basicConfig(level=args.loglevel.upper())

    client = SimpleClient(f'http://{args.hostname}/api/cdb_rest/')

    client.create_global_tag(args.gt)

    for i in range(args.n_pt):
        client.create_payload_type(f'my_pt_{i}')
        pll_name = client.get_payload_list_name(args.gt, f'my_pt_{i}')
        piov_list = get_random_piov_list(pll_name, args.n_iov)
        client.insert_payload_iov_list(piov_list)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--hostname', type=str, default='test111.apps.usatlas.bnl.gov')
    parser.add_argument('--gt', type=str, default='my_gt')
    parser.add_argument('--loglevel', choices=['warning', 'info', 'debug'], default='warning')
    parser.add_argument('--scenario', choices=['tiny', 'tiny-moderate', 'moderate', 'heavy-usage', 'worst-case'], default='warning')
    args = parser.parse_args()
    main(args)
