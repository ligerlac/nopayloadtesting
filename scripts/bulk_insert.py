import requests
import argparse


class BulkInserter:

    def __init__(self, params):
        self.params = params
        self.base_url = f'http://{params.hostname}/api/cdb_rest/'
        self.gt_statuses = ['unlocked']
        self.gt_names = [f'global_tag_{i}' for i in range(params.n_gt)]
        self.pt_names = [f'pl_type_{i}' for i in range(params.n_pt)]

    def get_payload_list_name(self, global_tag, pl_type):
        url = self.base_url + 'gtPayloadLists/' + global_tag
        res = requests.get(url).json()
        return res[pl_type]

    def get_existing_global_statuses(self):
        url = self.base_url + 'gtstatus'
        r = requests.get(url).json()
        return [gts['name'] for gts in r]

    def create_global_tag_statuses(self):
        print('create_global_tag_statuses()')
        existing = self.get_existing_global_statuses()
        for gts in list(set(self.gt_statuses).difference(existing)):
            print(f'creating global tag status {gts}...')
            self.create_global_tag_status(gts)

    def create_global_tag_status(self, name='unlocked'):
        url = self.base_url + 'gtstatus'
        r = requests.post(url=url, json={'name': name})

    def get_existing_global_tags(self):
        url = self.base_url + 'globalTags'
        r = requests.get(url).json()
        return [gt['name'] for gt in r]

    def create_global_tags(self):
        print('create_global_tags()')
        existing = self.get_existing_global_tags()
        for gt in list(set(self.gt_names).difference(existing)):
            print(f'creating global tag {gt}...')
            self.create_global_tag(gt)

    def create_global_tag(self, name):
        url = self.base_url + 'gt'
        r = requests.post(url=url, json={'status': 'unlocked', 'name': name})

    def get_existing_payload_types(self):
        url = self.base_url + 'pt'
        r = requests.get(url).json()
        return [pt['name'] for pt in r]

    def create_payload_types(self):
        existing = self.get_existing_payload_types()
        for pt in list(set(self.pt_names).difference(existing)):
            print(f'creating payload type {pt}...')
            self.create_payload_type(pt)

    def create_payload_type(self, name):
        url = self.base_url + 'pt'
        r = requests.post(url=url, json={'name': name})

    def create_payload_list(self, pl_type):
        url = self.base_url + 'pl'
        res = requests.post(url=url, json={'payload_type': pl_type}).json()
        return res['name']

    def attach_payload_list(self, gt, pl):
        url = self.base_url + 'pl_attach'
        res = requests.put(url=url, json={'payload_list': pl, 'global_tag': gt})
        print(res.json())

    def attach_payload_lists(self):
        for gt in self.gt_names:
            for pt in self.pt_names:
                try:
                    self.get_payload_list_name(gt, pt)
                    print(f'gt {gt} already has a pl for type {pt}')
                except KeyError:
                    pl_name = self.create_payload_list(pt)
                    print(f'created a pl of type {pt} with name {pl_name}')
                    print(f'attaching {pl_name} to {gt}')
                    self.attach_payload_list(gt, pl_name)

    def prepare(self):
        self.create_global_tag_statuses()
        self.create_global_tags()
        self.create_payload_types()
        self.attach_payload_lists()

    def insert(self):
        for gt in self.gt_names:
            for pt in self.pt_names:
                pll_name = self.get_payload_list_name(gt, pt)
                print(f'starting to inserting {self.params.last_iov - self.params.first_iov} iovs into pll {pll_name}')
                self.insert_iov(pll_name)
    
    def insert_iov(self, pll_name):
        url = self.base_url + 'bulk_piov'
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
                r = requests.post(url=url, json=piov_list)
                print(r)
                piov_list = []

        if piov_list:
            print(f'inserting the remaining {len(piov_list)} iovs... ')
            r = requests.post(url=url, json=piov_list)
            print(r)


def main(args):
    bulk_inserter = BulkInserter(args)
    bulk_inserter.prepare()
    bulk_inserter.insert()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--hostname", type=str, default="test111.apps.usatlas.bnl.gov")
    parser.add_argument("--n_gt", type=int, default=1)
    parser.add_argument("--n_pt", type=int, default=1)
    parser.add_argument("--first_iov", type=int, default=0)
    parser.add_argument("--last_iov", type=int, default=10)
    parser.add_argument("--bulk_size", type=int, default=5000)
    args = parser.parse_args()
    main(args)
