#!/usr/bin/bash

n_pt=10

for n_iov in 50000 100000 200000 300000 500000
do
  for pat in "first" "last" "random"
  do
    iov_per_pt=$(( $n_iov / $n_pt ))
    python scripts/bulk_insert.py --n_iov $iov_per_pt --n_pt $n_pt
    python run_campaign_mt.py --output output/MT/iov_scaling/$((n_pt))_$((iov_per_pt))/$pat/ --pattern $pat --nthreads 50 --ncalls 50
  done
done
