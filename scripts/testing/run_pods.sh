#!/usr/bin/bash

export NOPAYLOADCLIENT_CONF=sdcc.json
export HOSTNAME=test111.apps.usatlas.bnl.gov

n_pods=5

echo python run_campaign.py --output output/old_get/pod_scaling/$((n_pods))/constant/ --clientconf sdcc.json --pattern ccc --njobs 100 --ncalls 100
echo python run_campaign.py --output output/old_get/pod_scaling/$((n_pods))/random/ --clientconf sdcc.json --pattern rrr --njobs 100 --ncalls 100
