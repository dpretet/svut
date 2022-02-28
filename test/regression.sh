#!/usr/bin/env bash

# Get script's location
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# Try to create a testbench

echo "INFO: Execute svutCreate test"
"$DIR/../svutCreate" "$DIR/Adder.v"
ret=$?

if [[ $ret != 0 ]]; then
    echo "ERROR: Execution failed"
    exit 1
fi

if [ ! -e "Adder_testbench.sv" ]; then echo "ERROR: No testbench generated";  exit 1; fi
if [ ! -e "sim_main.cpp" ]; then echo "ERROR: No cpp testbench generated"; exit 1; fi
if [ ! -e "files.f" ]]; then echo "ERROR: No fileset file generated"; exit 1; fi

echo "Testsuite execution completed successfully ^^"


# First testsuite running over the adder, supposed to be successful

echo "INFO: Execute svutRun OK testsuite"
"$DIR/../svutRun" -test "$DIR/Adder_OK_testsuite.sv" -define "MYDEF1=5;MYDEF2" | tee log
ret=$?

if [[ $ret != 0 ]]; then
    echo "ERROR: Execution failed but should not..."
    exit 1
fi

echo "Testsuite execution completed successfully ^^"

# Second testsuite running over the adder, supposed to fail

echo "INFO: Execute svutRun KO testsuite"
"$DIR/../svutRun" -test "$DIR/Adder_KO_testsuite.sv" | tee log
ret=$?

error_num=9
# Count number of errors
ec=$(grep -c "ERROR:" log)

if [[ $ret == 0 ]]; then
    if [[ $ec != "$error_num" ]]; then
        echo "ERROR: Execution suffered $ec issues but not $error_num as expected ! "
        exit 1
    fi
else
    echo "ERROR: No errors detected while several exepected..."
    exit 1
fi

echo "Testsuite execution completed successfully ^^"
echo "Regression finished successfully. SVUT sounds alive ^^"
exit 0
