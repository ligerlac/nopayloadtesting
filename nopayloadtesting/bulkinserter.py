import requests
from nopayloadtesting.simpleclient import SimpleClient


class BulkInserter:

    def __init__(self, params):
        self.params = params
        self.base_url = f'http://{params.hostname}/api/cdb_rest/'
        self.base_inserter = SimpleClient(f'http://{params.hostname}/api/cdb_rest/')
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
            self.base_inserter.create_global_tag_status(gts)

    def get_existing_global_tags(self):
        url = self.base_url + 'globalTags'
        r = requests.get(url).json()
        return [gt['name'] for gt in r]

    def create_global_tags(self):
        print('create_global_tags()')
        existing = self.get_existing_global_tags()
        for gt in list(set(self.gt_names).difference(existing)):
            print(f'creating global tag {gt}...')
            self.base_inserter.create_global_tag(gt)

    def create_payload_types(self):
        existing = self.base_inserter.get_existing_payload_types()
        for pt in list(set(self.pt_names).difference(existing)):
            print(f'creating payload type {pt}...')
            self.base_inserter.create_payload_type(pt)

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
                    pl_name = self.base_inserter.create_payload_list(pt)
                    print(f'created a pl of type {pt} with name {pl_name}')
                    print(f'attaching {pl_name} to {gt}')
                    self.base_inserter.attach_payload_list(gt, pl_name)

    def prepare(self):
        self.create_global_tag_statuses()
        self.create_global_tags()
        self.create_payload_types()
        self.attach_payload_lists()

    def insert(self):
        for gt in self.gt_names:
            for pt in self.pt_names:
                plt_iov_dict = self.get_last_plt_iov_dict(gt)
                try:
                    first_iov = plt_iov_dict[pt] + 1
                except KeyError:
                    first_iov = 0
                pll_name = self.get_payload_list_name(gt, pt)
                print(f'starting to inserting iovs from {first_iov} to {self.params.n_iov} into pll {pll_name}')
                self.insert_iov(pll_name, first_iov)

    def insert_iov(self, pll_name, first_iov):
        url = self.base_url + 'bulk_piov'
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
                print(f'inserting {len(piov_list)} iovs... ')
                r = requests.post(url=url, json=piov_list)
                print(r)
                piov_list = []

        if piov_list:
            print(f'inserting the remaining {len(piov_list)} iovs... ')
            r = requests.post(url=url, json=piov_list)
            print(r)
