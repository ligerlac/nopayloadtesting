#!/usr/bin/bash

#for scenario in "tiny" "tiny-moderate" "moderate" "heavy-usage" "worst-case"
for scenario in "heavy-usage"
do
#  python scripts/scenario_insert.py --scenario $scenario
#  for endpoint in "payloadiovs" "payloadiovs2" "payloadiovstest"
  for endpoint in "payloadiovs" "payloadiovstest"
  do
    python run_campaign_mt.py --output output/MT/DEBUG_OFF/endpoints/$scenario/$endpoint/ --nthreads 50 --ncalls 50 --endpoint $endpoint
  done
done
