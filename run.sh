#!/usr/bin/bash

export NOPAYLOADCLIENT_CONF=sdcc.json
export HOSTNAME=test111.apps.usatlas.bnl.gov

last_n_iov=0
for n_iov in 100 1000 10000 100000 500000 1000000 2000000 3000000 4000000 5000000
do
    python scripts/bulk_insert.py --hostname $HOSTNAME --first_iov $last_n_iov --last_iov $n_iov 
    python run_campaign.py --output output/my_instance/iov_scaling/1_1_$n_iov/random/ --clientconf sdcc.json --pattern rrr --njobs 100 --ncalls 100
    python run_campaign.py --output output/my_instance/iov_scaling/1_1_$n_iov/constant/ --clientconf sdcc.json --pattern ccc --njobs 100 --ncalls 100
    last_n_iov=$n_iov
done
