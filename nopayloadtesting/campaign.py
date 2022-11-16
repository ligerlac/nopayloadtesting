import htcondor
import shutil
import time
import json
import subprocess
import os
from pathlib import Path

#d = {'const': '0', 'rand': f'$((RANDOM%{max_iov}))'}
#d = {'const': 'pl_type_0', 'rand': 'TODO'}
#d = {'const': 'global_tag_0', 'rand': 'TODO'}


class AccessPattern:
    # assumes (gt_i, pt_j, k) structure as defined in nopayloadclient example
    def __init__(self, pattern, db_size_dict):
        self.pattern = pattern
        self.n_gt = db_size_dict['n_global_tag']
        self.n_pt = db_size_dict['n_pt']
        self.n_iov = db_size_dict['n_iov_attached']
        print(f'initialized AP instance with pattern {pattern} and following db size:\n{db_size_dict}')

    def get_gt_expr(self):
        return 'global_tag_0'

    def get_pt_expr(self):
        return 'pl_type_0'

    def get_iov_expr(self):
        if self.pattern[2] == 'c':
            return '0'
        else:
            max_iov = int(self.n_iov / (self.n_gt * self.n_pt))
            return f'$((RANDOM%{max_iov}))'


class Campaign:
    def __init__(self, client_conf, n_jobs, n_calls, access_pattern, output):
        self.client_conf = client_conf
        self.n_jobs = n_jobs
        self.n_calls = n_calls
        self.access_pattern = access_pattern
        self.output = output
        self.db_size_dict = None
        self.cluster_id = None


    def prepare_output_folder(self):
        p = Path(Path.cwd() / self.output)
        shutil.rmtree(p, ignore_errors=True)
        p.mkdir(parents=True, exist_ok=True)
        p = Path(p / 'jobs/')
        shutil.rmtree(p, ignore_errors=True)
        p.mkdir(parents=True, exist_ok=True)


    def create_job(self):
        return htcondor.Submit({
            "executable": self.output + "/run.sh",
            "output": self.output + "/jobs/$(ProcId).out",
            "error": self.output + "/jobs/$(ProcId).err",
            "log": self.output + "/log.log",
            "requirements": '(Machine!="spool0679.sdcc.bnl.gov")&&(Machine!="spool0696.sdcc.bnl.gov")&&(Machine!="spool0870.sdcc.bnl.gov")&&(Machine!="spool0684.sdcc.bnl.gov")&&(Machine!="spool0685.sdcc.bnl.gov")&&(Machine!="spool0688.sdcc.bnl.gov")&&(Machine!="spool0693.sdcc.bnl.gov")&&(Machine!="spool0690.sdcc.bnl.gov")&&(Machine!="spool0695.sdcc.bnl.gov")&&(Machine!="spool0673.sdcc.bnl.gov")',
            "getenv": True
        })


    def submit(self):
        job = self.create_job()
        submit_result = htcondor.Schedd().submit(job, count=self.n_jobs)
        self.cluster_id = submit_result.cluster()
        print(f'submitted {self.n_jobs} jobs to cluster {self.cluster_id}')


    def wait_for_jobs_to_finish(self, t=10):
        while True:
            print(f'checking for cluster id {self.cluster_id}')
            q_status = htcondor.Schedd().query(
                constraint=f"ClusterId=={self.cluster_id}",
                projection=["ProcId", "JobStatus"])
            if not q_status:
                print('FINITO AMIGO')
                break
            print(f'{len(q_status)} job(s) still running. sleeping for {t} seconds')
            time.sleep(t)


    def write_config_to_file(self):
        with open(self.output + '/campaign_config.json', 'w') as f:
            json.dump(self.__dict__, f)


    def create_executable(self):
        string = '#!/usr/bin/bash\n'
        ### test curl google ###
        string += 'echo "testing node performance..."\n'
        string += 'start=`date +%s.%N`\n'
        string += 'httpcode=$(curl --write-out "%{http_code}" --silent --output /dev/null https://www.google.com)\n'
        string += 'end=`date +%s.%N`\n'
        string += 'runtime=$( echo "$end - $start" | bc -l)\n'
        string += 'echo "test curl took $runtime sec"\n'
        string += 'if (( $(echo "$runtime > 1" |bc -l) ))\n'
        string += 'then\n'
        string += '    echo "node is too slow, aborting..."\n'
        string += '    exit\n'
        string += 'fi\n'
        ### test ls ###
#        string += 'start=`date +%s.%N`\n'
#        string += 'eval "ls"\n'
#        string += 'end=`date +%s.%N`\n'
#        string += 'runtime=$( echo "$end - $start" | bc -l)\n'
#        string += 'echo "test ls took $runtime sec"\n'
        ### test for-loop ###
#        string += 'start=`date +%s.%N`\n'
#        string += 'for i in {1..100000}\n'
#        string += 'do\n'
#        string += '    j=i*i\n'
#        string += 'done\n'
#        string += 'end=`date +%s.%N`\n'
#        string += 'runtime=$( echo "$end - $start" | bc -l)\n'
#        string += 'echo "test for-loop took $runtime sec"\n'
        ap = AccessPattern(self.access_pattern, self.db_size_dict)
        gt = ap.get_gt_expr()
        pt = ap.get_pt_expr()
        iov = ap.get_iov_expr()
        string += f'for i in $(eval echo {{1..{self.n_calls}}})\n'
        string += 'do\n'
        string += f'  gt={gt}\n'
        string += f'  pt={pt}\n'
        string += f'  iov={iov}\n'
        string += '  echo requesting payload url for gt=$gt, pt=$pt, and iov=$iov\n'
        string += '  echo begin client: `date +%s%3N`\n'
        string += '  echo res=`./executables/cli_get $gt $pt $iov 0 `\n'
        string += '  echo end client: `date +%s%3N`\n'
        string += 'done\n'
    
        with open(self.output + '/run.sh', 'w') as f:
            f.write(string)

        os.chmod(self.output + '/run.sh', 0o755)


    def set_db_size_dict(self):
        print(os.environ["NOPAYLOADCLIENT_CONF"])
        x = subprocess.run('executables/check_size', capture_output=True)
        resp = x.stdout.decode("utf-8").split('\n')
        print(f'resp = {resp}')
        for line in resp:
            if "n_global_tag" in line:
                break
        print(f'line = {line}')
        x_dict = json.loads(line)
        x_dict = x_dict['msg']
        print(f'x_dict = {x_dict}')
        self.db_size_dict = x_dict


    def prepare(self):
        os.environ["NOPAYLOADCLIENT_CONF"] = self.client_conf
        self.prepare_output_folder()
        self.set_db_size_dict()
        self.create_executable()
        self.write_config_to_file()
