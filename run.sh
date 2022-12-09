#!/usr/bin/bash

export NOPAYLOADCLIENT_CONF=sdcc.json
export HOSTNAME=test111.apps.usatlas.bnl.gov

n_gt=1
n_pt=1

for n_iov in 0 1000000 2000000 3000000 4000000 5000000 7500000 10000000 15000000 20000000 50000000
#for n_iov in 0 100000 500000 1000000 2000000 3000000
#for n_iov in 0 1000 5000 10000 20000 30000
do
    python scripts/bulk_insert.py --hostname $HOSTNAME --n_iov $n_iov --n_pt $n_pt
    python run_campaign.py --output output/my_instance_5_pod/major_iov_scaling/$((n_gt))_$((n_pt))_$((n_iov))/random/ --clientconf sdcc.json --pattern rrr --njobs 100 --ncalls 100
    python run_campaign.py --output output/my_instance_5_pod/major_iov_scaling/$((n_gt))_$((n_pt))_$((n_iov))/constant/ --clientconf sdcc.json --pattern ccc --njobs 100 --ncalls 100
done
