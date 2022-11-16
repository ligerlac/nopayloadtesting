import argparse
from datetime import datetime
from nopayloadtesting.campaign import Campaign
from nopayloadtesting.summariser import Summariser


def main(args):
    campaign = Campaign(client_conf=args.clientconf, n_jobs=args.njobs, n_calls=args.ncalls, 
                       access_pattern='access_pattern', output=args.output)
    campaign.prepare()
    if args.dryrun:
        return
    campaign.submit()
    campaign.wait_for_jobs_to_finish()

    summariser = Summariser(args.output)
    summariser.extract_raw_results()
    summariser.save_raw_results()

    print(f'run_times = {summariser.run_times}')
    print(f'http_codes = {summariser.http_codes}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    date_str = datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")[:-3]
    parser.add_argument('--output', type=str, default=f'output/{date_str}', help='output folder') 
    parser.add_argument('--njobs', type=int, default=2, help='number of jobs') 
    parser.add_argument('--ncalls', type=int, default=2, help='number of calls to service by job')
    parser.add_argument('--executable', type=str, default='executables/client_lino.sh', help='path to executable')
    parser.add_argument('--clientconf', type=str, default='sdcc.json', help='name of nopayloadclient config file')
    parser.add_argument('--dryrun', action='store_true', default=False, help='dont submit the job')
    args = parser.parse_args()
    main(args)
