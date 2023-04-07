import argparse
import logging
from nopayloadtesting.simpleclient import SimpleClient
from nopayloadtesting.constants import MAX_IOV
import sys
import random


def main(args):

    logging.basicConfig(level=args.loglevel.upper())

    client = SimpleClient(f'http://{args.hostname}/api/cdb_rest/')
    client.clone_global_tag(args.source, args.target)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--hostname', type=str, default='localhost:8000')
    parser.add_argument('--loglevel', choices=['warning', 'info', 'debug'], default='warning')
    parser.add_argument('--source', type=str, default='heavy-usage')
    parser.add_argument('--target', type=str, default='heavy-usage-clone-1')
    args = parser.parse_args()
    main(args)
