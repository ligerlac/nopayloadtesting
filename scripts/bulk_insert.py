import requests
import argparse

class BulkInserter:

    def __init__(self, params):
        self.params = params

    def base_url(self):
        return f'http://{self.params.hostname}/api/cdb_rest/'

    def gt_names(self):
        return [f'global_tag_{i}' for i in range(self.params.n_gt)]

    def pt_names(self):
        return [f'pl_type_{i}' for i in range(self.params.n_pt)]

    def get_payloadlist_name(self, global_tag, pl_type):
        url = self.base_url() + 'gtPayloadLists/' + global_tag
        return requests.get(url).json()[pl_type]

    def insert(self):
        for gt in self.gt_names():
            for pt in self.pt_names():
                pll_name = self.get_payloadlist_name(gt, pt)
                print(f'starting to inserting {self.params.last_iov - self.params.first_iov} iovs into pll {pll_name}')
                self.insert_iov(pll_name)
    
    def insert_iov(self, pll_name):
        url = self.base_url() + 'bulk_piov'
        piov_list = []
        for iov in range(self.params.first_iov, self.params.last_iov):
            piov = {
                'payload_url': f'{pll_name}_{iov}_dummy_file.data',
                'payload_list': pll_name,
                'major_iov':  iov,
                'minor_iov': 0
            }
            piov_list.append(piov)
            if (iov+1) % self.params.bulk_size == 0:
                print(f'inserting {len(piov_list)} iovs... ')
                r = requests.post(url = url, json=piov_list)
                print(r)
                piov_list = []

        if piov_list:
            print(f'inserting the remaining {len(piov_list)} iovs... ')
            r = requests.post(url = url, json=piov_list)
            print(r)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--hostname", type=str, default="test111.apps.usatlas.bnl.gov")
    parser.add_argument("--n_gt", type=int, default=1)
    parser.add_argument("--n_pt", type=int, default=1)
    parser.add_argument("--first_iov", type=int, default=10)
    parser.add_argument("--last_iov", type=int, default=10)
    parser.add_argument("--bulk_size", type=int, default=5000)
    args = parser.parse_args()
    bulk_inserter = BulkInserter(args)
    bulk_inserter.insert()
#    print('main')
#    main(args)
