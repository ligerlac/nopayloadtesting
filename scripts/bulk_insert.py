from datetime import datetime
import requests
import argparse


class BulkInserter:

    def __init__(self, params):
        self.params = params
        self.base_url = f'http://{params.hostname}/api/cdb_rest/'
        self.gt_statuses = ['unlocked']
        self.gt_names = [f'global_tag_{i}' for i in range(params.n_gt)]
        self.pt_names = [f'pl_type_{i}' for i in range(params.n_pt)]
        self.n_iovs, self.begin_ts, self.end_ts, self.batch_sizes = [], [], [], []

    def get_payload_list_name(self, global_tag, pl_type):
        print(f'get_payload_list_name(global_tag={global_tag}, pl_type={pl_type})')
        url = self.base_url + 'gtPayloadLists/' + global_tag
        res = requests.get(url).json()
        print(f'res.json() = {res}')
        return res[pl_type]

    def get_existing_global_statuses(self):
        print('get_existing_global_tag_statuses()')
        url = self.base_url + 'gtstatus'
        res = requests.get(url).json()
        print(f'res.json() = {res}')
        return [gts['name'] for gts in res]

    def create_global_tag_statuses(self):
        print('create_global_tag_statuses()')
        existing = self.get_existing_global_statuses()
        for gts in list(set(self.gt_statuses).difference(existing)):
            print(f'creating global tag status {gts}...')
            self.create_global_tag_status(gts)

    def create_global_tag_status(self, name='unlocked'):
        print(f'create_global_tag_status(name={name})')
        url = self.base_url + 'gtstatus'
        res =requests.post(url=url, json={'name': name})
        print(f'res.json() = {res.json()}')

    def get_existing_global_tags(self):
        print('get_existing_global_tags()')
        url = self.base_url + 'globalTags'
        res =requests.get(url).json()
        print(f'res.json() = {res}')
        return [gt['name'] for gt in res]

    def create_global_tags(self):
        print('create_global_tags()')
        existing = self.get_existing_global_tags()
        for gt in list(set(self.gt_names).difference(existing)):
            print(f'creating global tag {gt}...')
            self.create_global_tag(gt)

    def create_global_tag(self, name):
        print(f'create_global_tag(name={name})')
        url = self.base_url + 'gt'
        res =requests.post(url=url, json={'status': 'unlocked', 'name': name, 'author': 'linogerlach'})
        print(f'res.json() = {res.json()}')

    def get_existing_payload_types(self):
        print(f'get_exisitng_payload_types()')
        url = self.base_url + 'pt'
        res =requests.get(url).json()
        print(f'res.json() = {res}')
        return [pt['name'] for pt in res]

    def create_payload_types(self):
        existing = self.get_existing_payload_types()
        for pt in list(set(self.pt_names).difference(existing)):
            print(f'creating payload type {pt}...')
            self.create_payload_type(pt)


    def create_payload_type(self, name):
        print(f'create_payload_type(name={name})')
        url = self.base_url + 'pt'
        res = requests.post(url=url, json={'name': name})
        print(f'res.json() = {res.json()}')

    def create_payload_list(self, pl_type):
        print(f'create_payload_list(pl_type={pl_type})')
        url = self.base_url + 'pl'
        res = requests.post(url=url, json={'payload_type': pl_type}).json()
        print(f'res.json() = {res}')
        return res['name']

    def attach_payload_list(self, gt, pl):
        print(f'attach_payload_list(gt={gt}, pl={pl})')
        url = self.base_url + 'pl_attach'
        res = requests.put(url=url, json={'payload_list': pl, 'global_tag': gt})
        print(f'res.json() = {res.json()}')

    def get_last_plt_iov_dict(self, global_tag):
        print('get_last_plt_iov_dict()')
        max_iov = 2147483647
        url = self.base_url + 'payloadiovs/?gtName=' + global_tag + '&majorIOV=' + str(max_iov) + '&minorIOV=0'
        print(f'url = {url}')
        last_plt_iov_dict = {}
        resp = requests.get(url)
        print(f'resp.json() = {resp.json()}')
        for obj in resp.json():
            last_plt_iov_dict[obj['payload_type']] = obj['payload_iov'][0]['major_iov']
        return last_plt_iov_dict

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
                try:
                    plt_iov_dict = self.get_last_plt_iov_dict(gt)
                    first_iov = plt_iov_dict[pt] + 1
                except Exception:
                    first_iov = 0
                pll_name = self.get_payload_list_name(gt, pt)
                print(f'starting to inserting iovs from {first_iov} to {self.params.n_iov} into pll {pll_name}')
                self.insert_iov(pll_name, first_iov)
    
    def insert_iov(self, pll_name, first_iov):
        piov_list = []
        for iov in range(first_iov, self.params.n_iov):
            piov = {
                'payload_url': f'{pll_name}_{iov}_dummy_file.data',
                'payload_list': pll_name,
                'major_iov': iov,
                'minor_iov': 0
            }
            piov_list.append(piov)
            if (iov+1) % self.params.bulk_size == 0:
                self.insert_piov_list(iov+1, piov_list)
                piov_list = []

        if piov_list:
            self.insert_piov_list(iov+1, piov_list)

    def insert_piov_list(self, n_iovs, piov_list):
        print(f'inserting {len(piov_list)} iovs... ')
        self.n_iovs.append(n_iovs)
        self.batch_sizes.append(len(piov_list))
        self.begin_ts.append(datetime.now())
        res = requests.post(url=self.base_url + 'bulk_piov', json=piov_list)
        self.end_ts.append(datetime.now())
        print(res)        

        


def main(args):
    bulk_inserter = BulkInserter(args)
    bulk_inserter.prepare()
    bulk_inserter.insert()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--hostname", type=str, default="test111.apps.usatlas.bnl.gov")
    parser.add_argument("--n_gt", type=int, default=1)
    parser.add_argument("--n_pt", type=int, default=1)
    parser.add_argument("--n_iov", type=int, default=0)
    parser.add_argument("--bulk_size", type=int, default=5000)
    parser.add_argument("--output", type=str, default=None)
    args = parser.parse_args()
    main(args)
