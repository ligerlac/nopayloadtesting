import argparse
import logging
import sys
import random
from nopayloadtesting.simpleclient import SimpleClient
from nopayloadtesting.constants import MAX_IOV
from datetime import datetime


def main(args):

    logging.basicConfig(level=args.loglevel.upper())

    client = SimpleClient(f'http://{args.hostname}/api/cdb_rest/')

    t_0 = datetime.now()
    #client.clone_global_tag('my_gt', 'clone_1') # took cloning took 0:01:14.505203
#    client.clone_global_tag('my_gt', 'clone_2')
    print(f'cloning took {datetime.now() - t_0}')



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--hostname', type=str, default='localhost:8000')
    parser.add_argument('--loglevel', choices=['warning', 'info', 'debug'], default='warning')
    args = parser.parse_args()
    main(args)
