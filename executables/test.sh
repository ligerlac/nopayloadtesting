#!/usr/bin/bash

echo "testing node performance..."
start=`date +%s.%N`
for i in {1..100000}
do
    j=i*i
done
end=`date +%s.%N`
runtime=$( echo "$end - $start" | bc -l)
echo "test for-loop took $runtime sec"

if (( $(echo "$runtime > 0.1" |bc -l) ))
then
  echo "node is too slow, aborting..."
  exit
fi

echo "DINGELING"
#for i in $(eval echo {1..$1})
#do
#    start=`date +%s.%N`
#    httpcode=$(curl --write-out '%{http_code}' --silent --output /dev/null http://test111.apps.usatlas.bnl.gov/api/cdb_rest/gt)
#    end=`date +%s.%N`
#    runtime=$( echo "$end - $start" | bc -l)
#    echo runtime=$runtime
#    echo httpcode=$httpcode
#done
