#!/usr/bin/env bash

# pipe fails if first command fails. Else is always successful
set -o pipefail
rm -f lint.txt; touch lint.txt

pylint -d C0301 -d C0103 ../svutRun.py | tee -a lint.txt
ret=$?

if [[ $ret != 0 ]]; then
    echo "Linting failed"
else
    echo "svutRun.py finished successfully"
fi

pylint -d C0301 -d C0103 ../svutCreate.py | tee -a lint.txt
ret=$?

if [[ $ret != 0 ]]; then
    echo "Linting failed"
else
    echo "svutCreate.py finished successfully"
fi

grep -n "^E:" lint.txt
ret=$?

if [[ $ret == 0 ]]; then
    echo "Linting failed"
    exit 1
else
    echo "Linting finished successfully"
    exit 0
fi
