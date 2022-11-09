import htcondor
import shutil
import time
import json
import subprocess
import os
from pathlib import Path


class AccessPattern:
    def __init__(self, name):
        self.name = name

    def gt(self):
        return 'sPHENIX_ExampleGT_1'

    def pt(self):
        return 'Beam'

    def iov(self):
        return '1'


class Campaign:
    def __init__(self, client_conf, n_jobs, n_calls, access_pattern, output):
        self.client_conf = client_conf
        self.n_jobs = n_jobs
        self.n_calls = n_calls
        self.access_pattern = access_pattern
        self.output = output
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
        total_conf = self.__dict__
        for key, value in self.get_db_size_dict().items():
            total_conf[key] = value
        with open(self.output + '/campaign_config.json', 'w') as f:
            json.dump(total_conf, f)


    def create_executable(self):
        string = '#!/usr/bin/bash\n'
        ap = AccessPattern(self.access_pattern)
        for i in range(self.n_calls):
            string += 'start=`date +%s.%N`\n'
            string += f'echo res=`./executables/cli_get {ap.gt()} {ap.pt()} {ap.iov()} 0 `\n'
            string += 'end=`date +%s.%N`\n'
            string += 'runtime=$( echo "$end - $start" | bc -l)\n'
            string += 'echo runtime=$runtime\n'
    
        with open(self.output + '/run.sh', 'w') as f:
            f.write(string)

        os.chmod(self.output + '/run.sh', 0o755)


    def get_db_size_dict(self):
        print(os.environ["NOPAYLOADCLIENT_CONF"])
        x = subprocess.run('executables/test_size', capture_output=True)
        x_dict = json.loads(x.stdout.decode("utf-8"))
        x_dict = x_dict['msg']
        return x_dict


    def prepare(self):
        os.environ["NOPAYLOADCLIENT_CONF"] = self.client_conf
        self.prepare_output_folder()
        self.create_executable()
        self.write_config_to_file()
