#!/usr/bin/env bash

# Get script's location
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# pipe fails if first command fails. Else is always successful
set -o pipefail


# First testsuite running over the adder, supposed to be successful

echo "INFO: Start Adder OK testsuite"
"$DIR/../svutRun" -test "Adder_OK_testsuite.sv" | tee log
ret=$?

if [[ $ret != 0 ]]; then
    echo "Execution failed"
    exit 1
else
    echo "Execution completed successfully"
fi


# Second testsuite running over the adder, supposed to fail

echo "INFO: Start Adder KO testsuite"
"$DIR/../svutRun" -test "Adder_KO_testsuite.sv" | tee log
ret=$?

error_num=7
# Count number of errors
ec=$(grep -c "ERROR:" log)

if [[ $ret == 0 ]]; then
    if [[ $ec != "$error_num" ]]; then
        echo "Execution suffered $ec issues but not $error_num as expected"
        exit 1
    fi
else
    echo "No errors detected while several exepected"
    exit 1
fi

echo "Regression finished successfully"
exit 0
