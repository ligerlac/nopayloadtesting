#!/usr/bin/bash

for n_threads in 1 2 5 10 20 50 100 200 500
do
  for pat in "random"
  do
    n_calls=$(( 10000 / $n_threads )) 
    python run_campaign_mt.py --output output/MT/pod_scaling/$((n_threads))_$((n_calls))/$pat/ --pattern $pat --nthreads $n_threads --ncalls $n_calls
  done
done
