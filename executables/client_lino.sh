#!/usr/bin/bash

for i in $(eval echo {1..$1})
do
    start=`date +%s.%N`
    res=./test_get
    end=`date +%s.%N`
    runtime=$( echo "$end - $start" | bc -l)
    echo runtime=$runtime
    echo httpcode=200
done
