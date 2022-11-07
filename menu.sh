#!/bin/bash

options[1]="Run the web server"
options[2]="Run the tests (pytest)"
options[3]="Run the static checks (mypy)"

for i in "${!options[@]}"; do echo "$i - ${options[$i]}"; done
echo -n "Type what to do > "
response=
read response

source /application/env_correlation/bin/activate
cd /application/correlation
if [ "$response" = "1" ]; then
    ./run_server.py "0.0.0.0"
fi
if [ "$response" = "2" ]; then
    ./run_tests.sh
fi
if [ "$response" = "3" ]; then
    ./run_mypy.sh
fi
