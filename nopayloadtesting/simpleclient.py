import requests
import logging
import math
from nopayloadtesting.constants import MAX_IOV


class SimpleClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.payload_lists = {}

    def create_global_tag_status(self, name='unlocked'):
        url = self.base_url + 'gtstatus'
        r = requests.post(url=url, json={'name': name})
        logging.info(r.json())

    def create_global_tag(self, name):
        self.create_global_tag_status('unlocked')
        url = self.base_url + 'gt'
        r = requests.post(url=url, json={'status': 'unlocked', 'name': name})
        logging.info(r.json())

    def create_payload_type(self, name):
        url = self.base_url + 'pt'
        r = requests.post(url=url, json={'name': name})
        logging.info(r.json())

    def create_payload_list(self, pl_type):
        url = self.base_url + 'pl'
        r = requests.post(url=url, json={'payload_type': pl_type})
        logging.info(r.json())
        return r.json()['name']

    def attach_payload_list(self, gt, pl):
        url = self.base_url + 'pl_attach'
        r = requests.put(url=url, json={'payload_list': pl, 'global_tag': gt})
        logging.info(r.json())

    def get_existing_payload_types(self):
        url = self.base_url + 'pt'
        r = requests.get(url)
        logging.info(r.json())
        return [pt['name'] for pt in r.json()]

    def create_payload_iov(self, major_iov, minor_iov, payload_url):
        url = self.base_url + 'piov'
        j = {'payload_url': payload_url,
             'major_iov': major_iov,
             'minor_iov': minor_iov,
             'checksum': 'checksum'}
        r = requests.post(url=url, json=j)
        logging.info(r.json())
        return r.json()['id']

    def attach_payload_iov(self, pll_name, piov_id):
        url = self.base_url + 'piov_attach'
        j = {"payload_list": pll_name,
             "piov_id": piov_id}
        r = requests.put(url=url, json=j)
        logging.info(r.json())

    def get_payload_lists(self, global_tag):
        url = self.base_url + 'gtPayloadLists/' + global_tag
        r = requests.get(url)
        logging.info(r.json())
        return r.json()

    def gt_has_pl_type(self, gt, pt):
        payload_lists = self.get_payload_lists(gt)
        for pll_name in payload_lists:
            if pll_name == pt:
                return True
        return False

    def insert_payload_iov_list(self, piov_list):
        url = self.base_url + 'bulk_piov'
        bulk_size = 5000
        for i in range(math.ceil(len(piov_list)/bulk_size)):
            tmp_list = piov_list[i*bulk_size:(i+1)*bulk_size]
            logging.info(f'inserting {len(tmp_list)} iovs... ')
            r = requests.post(url=url, json=tmp_list)
            logging.info(r)

    def get_payload_list_name(self, gt, pt):
        payload_lists = self.get_payload_lists(gt)
        if pt in payload_lists:
            pll_name = payload_lists[pt]
        else:
            pll_name = self.create_payload_list(pt)
            self.attach_payload_list(gt, pll_name)
        return pll_name

    def insert_payload_iov(self, gt, pt, url, major_start, minor_start):
        pll_name = self.get_payload_list_name(gt, pt)
        piov_id = self.create_payload_iov(major_start, minor_start, url)
        self.attach_payload_iov(pll_name, piov_id)

    def clone_global_tag(self, source, target):
        url = self.base_url + 'cloneGlobalTag/' + source + '/' + target
        r = requests.post(url)
        logging.info(r.json())



    """
    def prepareInsertIov(self, Payload &pl):
        checkGtExists(global_tag_);
        checkPlTypeExists(pl.type);
        if (!gtHasPlType(pl.type)) {
            std::cout << "gt " << global_tag_ << " has no pl type " << pl.type << std::endl;
            std::cout << "attempting to attach it..." << std::endl;
            createNewPll(pl.type);
        }
    }
    """