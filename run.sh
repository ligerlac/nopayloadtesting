#!/usr/bin/bash

export export NOPAYLOADCLIENT_CONF=sdcc.json
./executables/check_size

#for n_iov in 1 10 100 1000 2000 3000 4000 5000 6000 7000 8000 9000 10000
#for n_iov in 12000 14000 16000 18000 20000 25000 30000 35000 40000 45000 50000
for n_iov in 45000 50000
do
    ./executables/insert_performance_evaluation 1 1 $n_iov
    python run_campaign.py --output output/my_instance/iov_scaling/1_1_$n_iov/random/ --clientconf sdcc.json --pattern rrr --njobs 100 --ncalls 100
    python run_campaign.py --output output/my_instance/iov_scaling/1_1_$n_iov/constant/ --clientconf sdcc.json --pattern ccc --njobs 100 --ncalls 100
done
