#!/usr/bin/bash

n_pt=1

for n_iov in 50000 100000 200000 300000 500000 1000000
do
  for pat in "frr" "fff" "fll"
  do
    iov_per_pt=$(( $n_iov / $n_pt ))
    python scripts/bulk_insert.py --hostname $HOSTNAME --n_gt $n_gt --n_iov $iov_per_pt --n_pt $n_pt
    python run_campaign.py --output output/patterns/$((n_gt))_$((n_pt))_$((iov_per_pt))/$pat/ --clientconf $NOPAYLOADCLIENT_CONF --pattern $pat --njobs 100 --ncalls 100
  done
done
