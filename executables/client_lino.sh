#!/usr/bin/bash

useage="$0 <nopayloadclient conf name> <n_calls>"

export NOPAYLOADCLIENT_CONF=$1

for i in $(eval echo {1..$2})
do
    start=`date +%s.%N`
    ./cli_get sPHENIX_ExampleGT_1 Beam 0 0
    end=`date +%s.%N`
    runtime=$( echo "$end - $start" | bc -l)
    echo runtime=$runtime
done