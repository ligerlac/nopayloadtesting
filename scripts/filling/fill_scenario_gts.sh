#!/usr/bin/bash

#for scenario in "tiny" "tiny-moderate" "moderate" "heavy-usage"
for scenario in "worst-case"
do
  python random_scenario_insert.py --hostname test111.apps.usatlas.bnl.gov --scenario $scenario --gt $scenario
done
