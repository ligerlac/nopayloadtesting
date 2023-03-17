import requests
import sys


base_url = "http://localhost:8000/api/cdb_rest/"


def create_global_tag_status(name):
    url = base_url + 'gtstatus'
    r = requests.post(url=url, json={'name': name})
    print(f'r.text={r.text}')


def create_global_tag(name):
    url = base_url + "gt"
    r = requests.post(url=url, json={'status': 'unlocked', 'name': name})
    print(f'r.text={r.text}')


def create_payload_type(name):
    url = base_url + 'pt'
    r = requests.post(url=url, json={'name': name})
    print(f'r.text={r.text}')


def create_payload_list(pt):
    url = base_url + 'pl'
    res = requests.post(url=url, json={'payload_type': 'pt_0'}).json()
    return res['id']


def attach_payload_list(gt, pl):
    url = base_url + 'pl_attach'
    res = requests.put(url=url, json={'payload_list': pl, 'global_tag': gt})


if __name__ == '__main__':
    create_global_tag_status('unlocked')
    create_global_tag('my_gt')
    create_payload_type('my_pt')
    create_payload_list('my_pt')
