#!/usr/bin/bash

useage="$0 <client_config> <n_calls>"

#export NOPAYLOADCLIENT_CONF=sdcc.json
export NOPAYLOADCLIENT_CONF=$1

echo size=`./executables/test_size`

for i in $(eval echo {1..$2})
do
    start=`date +%s.%N`
    echo res=`./executables/cli_get sPHENIX_ExampleGT_1 Beam 0 0`
    end=`date +%s.%N`
    runtime=$( echo "$end - $start" | bc -l)
    echo runtime=$runtime
done
