#!/usr/bin/bash


for n_pt in 10 20 30 40 50
do
  for n_iov in 1000 2000 3000 4000 5000
  do
    python scripts/bulk_insert.py --n_iov $n_iov --n_pt $n_pt
    for endpoint in "payloadiovs" "payloadiovs2" "payloadiovsfast" "payloadiovstest"
    do
      python run_campaign_mt.py --output output/MT/endpoints/$((n_pt))_$((n_iov))/$endpoint/ --nthreads 50 --ncalls 50 --endpoint $endpoint
    done
  done
  curl -X DELETE "http://test111.apps.usatlas.bnl.gov/api/cdb_rest/deleteGlobalTag/global_tag_0"
done
