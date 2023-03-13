import requests
import argparse
import sys
from bulk_insert import BulkInserter


def main(args):
    args.n_gt = 1
    args.bulk_size = 5000
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
    bulk_inserter = BulkInserter(args)
    bulk_inserter.prepare()
    bulk_inserter.insert()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--hostname", type=str, default="test111.apps.usatlas.bnl.gov")
    parser.add_argument("--scenario", type=str, default="tiny")
    args = parser.parse_args()
    main(args)
