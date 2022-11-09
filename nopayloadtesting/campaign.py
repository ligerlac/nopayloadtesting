import htcondor
import shutil
import time
import json
import subprocess
import os
from pathlib import Path


class AccessPattern:
    # assumes (gt_i, pt_j, k) structure as defined in nopayloadclient example
    def __init__(self, name, db_size_dict):
        self.name = name
        self.n_gt = db_size_dict['n_global_tag']
        self.n_pt = db_size_dict['n_pt']
        self.n_iov = db_size_dict['n_iov_attached']
        print(f'initialized AP instance with name {name} and following db size:\n{db_size_dict}')

    def gt(self):
        return 'gt_0'

    def pt(self):
        return 'pt_0'

    def get_iov_expr(self):
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
        ap = AccessPattern(self.access_pattern, self.db_size_dict)
        iov = ap.get_iov_expr()
        for i in range(self.n_calls):
            string += 'start=`date +%s.%N`\n'
            string += f'echo res=`./executables/cli_get {ap.gt()} {ap.pt()} {iov} 0 `\n'
            string += 'end=`date +%s.%N`\n'
            string += 'runtime=$( echo "$end - $start" | bc -l)\n'
            string += 'echo runtime=$runtime\n'
    
        with open(self.output + '/run.sh', 'w') as f:
            f.write(string)

        os.chmod(self.output + '/run.sh', 0o755)


    def set_db_size_dict(self):
        x = subprocess.run('executables/check_size', capture_output=True)
        x_dict = json.loads(x.stdout.decode("utf-8"))
        x_dict = x_dict['msg']
        self.db_size_dict = x_dict


    def prepare(self):
        os.environ["NOPAYLOADCLIENT_CONF"] = self.client_conf
        self.prepare_output_folder()
        self.set_db_size_dict()
        self.create_executable()
        self.write_config_to_file()
