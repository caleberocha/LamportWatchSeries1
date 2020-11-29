#!/bin/bash

for i in 1 2 3 4 5; do
    curl http://dontpad.com/calebe/lamport/$i \
        -H 'Content-Type: application/x-www-form-urlencoded;charset=UTF-8' \
        --data-raw 'text=' \
        --compressed \
        --insecure
done
