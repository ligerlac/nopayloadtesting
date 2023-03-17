import argparse
import logging
import sys
import random
from nopayloadtesting.simpleclient import SimpleClient
from nopayloadtesting.constants import MAX_IOV


def main(args):

    logging.basicConfig(level=args.loglevel.upper())

    client = SimpleClient(f'http://{args.hostname}/api/cdb_rest/')

    client.create_global_tag('my_small_gt')
    client.create_payload_type('my_first_pt')
    client.create_payload_type('my_second_pt')

    client.insert_payload_iov('my_small_gt', 'my_first_pt', 'my_first_pt_0_0.dat', 0, 0)
    client.insert_payload_iov('my_small_gt', 'my_first_pt', 'my_first_pt_0_1.dat', 0, 1)
    client.insert_payload_iov('my_small_gt', 'my_second_pt', 'my_second_pt_0_0.dat', 0, 0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--hostname', type=str, default='localhost:8000')
    parser.add_argument('--loglevel', choices=['warning', 'info', 'debug'], default='warning')
    args = parser.parse_args()
    main(args)
