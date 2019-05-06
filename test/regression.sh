#!/usr/bin/env bash

# pipe fails if first command fails. Else is always successful
set -o pipefail
rm -f regression.txt; touch regression.txt
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
error_num=7

$DIR/../svutRun -test "Adder_unit_test_OK.sv" | tee -a regression.txt
ret=$?

if [[ $ret != 0 ]]; then
    echo "Execution failed"
else
    echo "Execution completed successfully"
fi

$DIR/../svutRun -test "Adder_unit_test_KO.sv" | tee -a regression.txt
ret=$?
ec=$(grep -c "ERROR:" regression.txt)

if [[ $ret == 0 ]]; then
    if [[ $ec != "$error_num" ]]; then
        echo "Execution suffered $ec issues but not $error_num as expected"
        exit 1
    else
        echo "Regression finished successfully"
        exit 0
    fi
else
    echo "No errors detected while several exepected"
    exit 1
fi
