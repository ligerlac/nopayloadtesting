#!/usr/bin/bash

for i in $(eval echo {1..$1})
do
    start=`date +%s.%N`
    httpcode=$(curl --write-out '%{http_code}' --silent --output /dev/null http://test111.apps.usatlas.bnl.gov/api/cdb_rest/gt)
    end=`date +%s.%N`
    runtime=$( echo "$end - $start" | bc -l)
    echo runtime=$runtime
    echo httpcode=$httpcode
done
