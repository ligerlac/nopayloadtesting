#!/usr/bin/bash

for n_threads in 1 2 5 10 20 50 100 200 500
do
#  for pat in "first" "last" "random"
  for pat in "first"
  do
    n_calls=$(( 10000 / $n_threads )) 
#    python run_campaign_mt.py --output output/MT/thread_scaling/$((n_threads))_$((n_calls))/$pat/ --pattern $pat --nthreads $n_threads --ncalls $n_calls
    python run_campaign_mt.py --output output/MT/new_thread_scaling/$((n_threads))_$((n_calls))/$pat/ --pattern $pat --nthreads $n_threads --ncalls $n_calls
  done
done
