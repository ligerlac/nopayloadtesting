import argparse
from nopayloadtesting.campaign import Campaign
from nopayloadtesting.summariser import Summariser


def main(args):
    campaign = Campaign(args.executable, args.njobs, args.ncalls, args.output)
    campaign.prepare_output_folder()
    campaign.write_config_to_file()
    campaign.submit()
    campaign.wait_for_jobs_to_finish()

    summariser = Summariser(args.output)
    summariser.extract_raw_results()
    summariser.save_raw_results()

    print(f'run_times = {summariser.run_times}')
    print(f'http_codes = {summariser.http_codes}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=str, default='output/latest', help='output folder') 
    parser.add_argument('--njobs', type=int, default=2, help='number of jobs') 
    parser.add_argument('--ncalls', type=int, default=2, help='number of calls to service by job')
    parser.add_argument('--executable', type=str, default='executables/curl_lino.sh', help='path to executable')
    args = parser.parse_args()
    main(args)
