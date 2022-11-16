## Welcome to nopayloadtesting!
### Table of contents
* [Introduction](#introduction)
* [Setup](#setup)
* [Usage](#usage)

### Introduction
This code base is for testing the performance of a database
through HTCondor jobs.

### Setup
If not already existent, create venv and install requirements:
```
python -m venv venv/
. venv/bin/activate
pip install -r requirements.txt
```

### Usage
The workflow is as follows:
* reset the DB: go to https://console-openshift-console.apps.usatlas.bnl.gov/
 -> 'Workloads' -> 'Pods' -> 'Terminal'. Pick the 'postgresql' pod and go to Terminal.
type 'psql' and paste following code:
```
\c sampledb
TRUNCATE "GlobalTag" CASCADE;
TRUNCATE "GlobalTagStatus" CASCADE;
TRUNCATE "PayloadIOV" CASCADE;
TRUNCATE "PayloadList" CASCADE;
TRUNCATE "PayloadListIdSequence" CASCADE;
TRUNCATE "PayloadType" CASCADE;
```
* populate the DB with example data
```
./executables/insert_performance_evaluation <n_gt> <n_pt> <n_iov>
```
where <n_gt> is the number of GlobalTags, <n_pt> is the number of PayloadTypes
per global tag and <n_iov> is the number of PayloadIOVs per PayloadType and
GlobalTag.
* run a new campaign:
```
python run_campaign.py
```