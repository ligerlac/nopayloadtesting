#!/usr/bin/bash

for scenario in "tiny" "tiny-moderate" "moderate" "heavy-usage" "worst-case"
do
  python scripts/scenario_insert.py --scenario $scenario > /dev/null
  curl "http://test111.apps.usatlas.bnl.gov/api/cdb_rest/globalTags"
done
