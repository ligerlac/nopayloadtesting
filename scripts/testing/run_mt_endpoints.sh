#!/usr/bin/bash

for n_iov in 1000 2000 3000 4000 5000
do
  python random_insert.py --hostname localhost:8000 --n_pt 100 --n_iov 1000
  for endpoint in "payloadiovs" "payloadiovstest" "payloadiovssql"
  do
    echo $endpoint
    python run_campaign_mt.py --output output/MT/local/endpoints/$n_iov/$endpoint/ --nthreads 1 --ncalls 200\
     --endpoint $endpoint --hostname localhost:8000
  done
done
