#!/usr/bin/env bash

# Get script's location
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# pipe fails if first command fails. Else is always successful
set -o pipefail


# First testsuite running over the adder, supposed to be successful

"$DIR/../svutRun" -test "Adder_OK_testsuite.sv" -define "MYDEF1=5;MYDEF2" | tee log
ret=$?

if [[ $ret != 0 ]]; then
    echo "Execution failed but should not..."
    exit 1
else
    echo "OK testsuite execution completed successfully ^^"
fi


# Second testsuite running over the adder, supposed to fail

"$DIR/../svutRun" -test "Adder_KO_testsuite.sv" | tee log
ret=$?

error_num=9
# Count number of errors
ec=$(grep -c "ERROR:" log)

if [[ $ret == 0 ]]; then
    if [[ $ec != "$error_num" ]]; then
        echo "Execution suffered $ec issues but not $error_num as expected ! "
        exit 1
    else
        echo "KO testsuite execution completed successfully ^^"
    fi
else
    echo "No errors detected while several exepected..."
    exit 1
fi

echo "Regression finished successfully. SVUT sounds alive ^^"
exit 0
