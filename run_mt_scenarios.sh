#!/usr/bin/bash

for scenario in "tiny" "tiny-moderate" "moderate" "heavy-usage" "worst-case"
do
  python scripts/scenario_insert.py --scenario $scenario
  for pat in "first" "last" "random"
  do
    python run_campaign_mt.py --output output/MT/scenarios/$scenario/$pat/ --pattern $pat --nthreads 50 --ncalls 50
  done
done
