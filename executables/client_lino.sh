#!/usr/bin/bash

useage="$0 <n_calls>"

export NOPAYLOADCLIENT_CONF=sdcc.json

./executables/test_size

for i in $(eval echo {1..$1})
do
    start=`date +%s.%N`
    ./executables/cli_get sPHENIX_ExampleGT_1 Beam 0 0
    end=`date +%s.%N`
    runtime=$( echo "$end - $start" | bc -l)
    echo runtime=$runtime
done
