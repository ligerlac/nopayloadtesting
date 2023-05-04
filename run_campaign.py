import argparse
import asyncio
import random
from datetime import datetime
import numpy as np
from aiohttp import ClientSession
import concurrent.futures
import requests
import logging


MAX_IOV = 2147483647


class RequestMaker:

    def __init__(self, host_name, end_point, global_tag, pattern):
        self.pattern = pattern
        self.base_url = f'http://{host_name}/api/cdb_rest/{end_point}/?gtName={global_tag}'

    def get_piov_url(self):
        major = {'first': 0, 'last': MAX_IOV, 'random': random.randint(0, MAX_IOV)}[self.pattern]
        minor = {'first': 0, 'last': MAX_IOV, 'random': random.randint(0, MAX_IOV)}[self.pattern]
        return f'{self.base_url}&majorIOV={major}&minorIOV={minor}'

    def make_requests(self, n):
        raise NotImplemented


class AsyncRequestMaker(RequestMaker):

    def make_requests(self, n):
        return asyncio.run(self._make_requests(n))

    async def make_request(self, session: ClientSession, queue: asyncio.Queue):
        url = self.get_piov_url()
        beg_ts = datetime.now().timestamp()
        async with session.get(url) as response:
            await queue.put((beg_ts, datetime.now().timestamp(), response))

    async def _make_requests(self, n):
        results = []
        queue = asyncio.Queue()

        async with ClientSession() as session:
            async with asyncio.TaskGroup() as group:
                for _ in range(n):
                    group.create_task(self.make_request(session, queue))

        while not queue.empty():
            results.append(await queue.get())

        return results


class ThreadingRequestMaker(RequestMaker):

    def make_requests(self, n):
        urls = [self.get_piov_url() for _ in range(n)]
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            results = executor.map(self.make_request, urls)
        return results

    def make_request(self, url):
        beg_ts = datetime.now().timestamp()
        res = requests.get(url)
        return beg_ts, datetime.now().timestamp(), res


def main(args):
    logging.getLogger().setLevel(args.log_level)

    cls_dict = {'threading': ThreadingRequestMaker, 'async': AsyncRequestMaker}
    MakerClass = cls_dict[args.style]
    req_maker = MakerClass(args.hostname, args.endpoint, args.gt, args.pattern)

    wall_beg = datetime.now().timestamp()
    results = req_maker.make_requests(args.ncalls)
    wall_duration = datetime.now().timestamp() - wall_beg
    print(f'campaign took {wall_duration}')

    durations, beg_ts, end_ts = [], [], []
    for p in results:
        beg_ts.append(p[0])
        end_ts.append(p[1])
        durations.append(p[1] - p[0])
    
    print(f'made {args.ncalls} calls within {np.max(beg_ts) - np.min(beg_ts)}')
    print(f'mean response time [ms]: {round(np.mean(durations) * 1000)}')
    print(f'mean response frequency [Hz]: {round(args.ncalls/wall_duration, 2)}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    date_str = datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f')[:-3]
    parser.add_argument('--output', type=str, default=f'output/{date_str}', help='output folder')
    parser.add_argument('--hostname', type=str, default='test111.apps.usatlas.bnl.gov')
    parser.add_argument('--ncalls', type=int, default=10, help='number of total calls to service')
    parser.add_argument('--pattern', type=str, default='random', choices=['random', 'first', 'last'])
    parser.add_argument('--style', type=str, default='async', choices=['async', 'threading', 'htc'])
    parser.add_argument('--endpoint', type=str, default='payloadiovs')
    parser.add_argument('--gt', type=str, default='my_gt')
    parser.add_argument('-l', '--log-level', choices=['DEBUG', 'INFO', 'WARNING'],
                        default='WARNING')
    args = parser.parse_args()
    main(args)
