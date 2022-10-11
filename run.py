import argparse
import re, glob
from nopayloadtesting.campaign import Campaign


def extract_run_times_and_http_codes(output_path):
    run_times = []
    http_codes = []
    for fn in glob.iglob(f'{output_path}/*out'):
        print(f'fn = {fn}')
        with open(fn, 'r') as f:
            for line in f:
                if re.search('runtime', line):
                    run_times.append(float(line.split('runtime=')[1].strip()))
                if re.search('httpcode', line):
                    http_codes.append(int(line.split('httpcode=')[1].strip()))
    return run_times, http_codes


def main(args):
    campaign = Campaign(args.executable, args.njobs, args.ncalls, args.output)
    campaign.prepare_output_folder()
    campaign.submit()
    campaign.wait_for_jobs_to_finish()
    
    run_times, http_codes = extract_run_times_and_http_codes(args.output)

    print(f'run_times = {run_times}')
    print(f'http_codes = {http_codes}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=str, default='output/latest', help='output folder') 
    parser.add_argument('--njobs', type=int, default=2, help='number of jobs') 
    parser.add_argument('--ncalls', type=int, default=2, help='number of calls to service by job')
    parser.add_argument('--executable', type=str, default='executables/curl_lino.sh', help='path to executable')
    args = parser.parse_args()
    main(args)
