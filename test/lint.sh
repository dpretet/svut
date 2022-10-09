#!/usr/bin/env bash

# pipe fails if first command fails. Else is always successful
set -o pipefail
rm -f lint.txt; touch lint.txt
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

echo "Lint svutRun.py"
pylint -d C0301 -d C0103 $DIR/../svut/svutRun.py | tee -a lint.txt
ret=$?

if [[ $ret != 0 ]]; then
    echo "Linting failed"
else
    echo "svutRun.py finished successfully"
fi

echo "Lint svutCreate.py"
pylint -d C0301 -d C0103 $DIR/../svut/svutCreate.py | tee -a lint.txt
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
