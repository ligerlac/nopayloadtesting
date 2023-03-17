import argparse
from nopayloadtesting.bulkinserter import BulkInserter


def main(args):
    bulk_inserter = BulkInserter(args)
    bulk_inserter.prepare()
    bulk_inserter.insert()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--hostname', type=str, default='test111.apps.usatlas.bnl.gov')
    parser.add_argument('--n_gt', type=int, default=1)
    parser.add_argument('--n_pt', type=int, default=1)
    parser.add_argument('--n_iov', type=int, default=0)
    parser.add_argument('--bulk_size', type=int, default=5000)
    args = parser.parse_args()
    main(args)
