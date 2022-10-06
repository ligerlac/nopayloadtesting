start=`date +%s.%N`
resp=$(curl --write-out '%{http_code}' --silent --output /dev/null http://linostest.apps.usatlas.bnl.gov/api/cdb_rest/gt)
end=`date +%s.%N`
runtime=$( echo "$end - $start" | bc -l)
echo runtime=$runtime
echo resp=$resp
