#!/bin/bash

for i in 1 2 3 4 5; do
    echo Clearing log $i
    curl http://dontpad.com/calebe/lamport/$i -H 'Content-Type: application/x-www-form-urlencoded;charset=UTF-8' --data-raw 'text='
    echo ''
done
