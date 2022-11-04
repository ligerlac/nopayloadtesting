import htcondor
import shutil
import time
import json
import subprocess
from pathlib import Path


class Campaign:
    def __init__(self, executable, client_conf, n_jobs, n_calls, output):
        self.executable = executable
        self.client_conf = client_conf
        self.n_jobs = n_jobs
        self.n_calls = n_calls
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
            "executable": self.executable,
            "arguments": f"{self.client_conf} {self.n_calls}",
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

    def get_db_size_dict(self):
        x = subprocess.run('executables/test_size', capture_output=True)
        x_dict = json.loads(x.stdout.decode("utf-8"))
        x_dict = x_dict['msg']
        return x_dict
