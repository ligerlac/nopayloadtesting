import json
import argparse
import htcondor


def main(args):
    with open(args.conf) as f:
        conf_dict = json.load(f)

    hostname_job = htcondor.Submit({
        "executable": "/bin/hostname",  # the program to run on the execute node
        "output": "hostname.out",       # anything the job prints to standard output will end up in this file
        "error": "hostname.err",        # anything the job prints to standard error will end up in this file
        "log": "hostname.log",          # this file will contain a record of what happened to the job
        "request_cpus": "1",            # how many CPU cores we want
        "request_memory": "128MB",      # how much memory we want
        "request_disk": "128MB",        # how much disk space we want
    })

    print(hostname_job)

    schedd = htcondor.Schedd()                   # get the Python representation of the scheduler
    submit_result = schedd.submit(hostname_job)  # submit the job
    print(submit_result.cluster())               # print the job's ClusterId

 
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--conf', type=str, default='conf/lino.json', help='path to config file') 
    args = parser.parse_args()
    main(args)
