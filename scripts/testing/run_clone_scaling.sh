#!/usr/bin/bash

for endpoint in "payloadiovs" "payloadiovstest" "payloadiovssql"
do
  python run_campaign_mt.py --output output/MT/local/clones/0/$endpoint/ --nthreads 1\
   --ncalls 20 --endpoint $endpoint --hostname localhost:8000 --pattern last
done

for i in {1..200}
do
  echo "creating clone number $i"
  time curl -X POST "localhost:8000/api/cdb_rest/cloneGlobalTag/my_gt/clone_$i" > /dev/null
  for endpoint in "payloadiovs" "payloadiovstest" "payloadiovssql"
  do
    python run_campaign_mt.py --output output/MT/local/clones/$i/$endpoint/ --nthreads 1\
     --ncalls 20 --endpoint $endpoint --hostname localhost:8000 --pattern last
  done
done
