import json
import argparse
import htcondor
from pathlib import Path


def get_exec_string(conf_dict):
    with open(conf_dict['executable'], 'r') as f:
        exec_string_ = f.read()
    exec_string = ""
    for i in range(conf_dict['calls_per_job']):
        exec_string += exec_string_ + '\n'
    return exec_string


def main(args):
    with open(args.conf) as f:
        conf_dict = json.load(f)

    exec_string = get_exec_string(conf_dict)
    exec_file = Path.cwd() / args.output / "executable.sh"
    exec_file.write_text(exec_string)

    job = htcondor.Submit({
        "executable": args.output + "/executable.sh",
        "output": args.output + "/$(ProcId).out",
        "error": args.output + "/$(ProcId).err",
        "log": args.output + "/log.log"
    })

    schedd = htcondor.Schedd()
    submit_result = schedd.submit(job, count=conf_dict["calls_per_job"])
    print(submit_result.cluster())


 
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--conf', type=str, default='conf/lino.json', help='path to config file') 
    parser.add_argument('--output', type=str, default='output/', help='output folder') 
    args = parser.parse_args()
    main(args)
