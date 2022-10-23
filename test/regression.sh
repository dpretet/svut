#!/usr/bin/env bash

# Global status, the global return code
status=0

#------------------------------------------------------------------------------
# Bash compliant way to check a program is in PATH
# https://stackoverflow.com/a/53798785
#------------------------------------------------------------------------------
function is_bin_in_path {

  builtin type -P "$1" &> /dev/null
}


#------------------------------------------------------------------------------
# Prepare Bats, if not present in PATH, clone it locally and setup in PATH.
# If not present and bats folder is already there, just setup PATH. Else just
# exit gently
#------------------------------------------------------------------------------
setup_bats() {

    if is_bin_in_path bats ; then
        echo 'INFO: Bats in PATH'
        return 0
    else
        echo 'INFO: Bats not in PATH'
        [ ! -d "$DIR/bats" ] && git clone https://github.com/bats-core/bats-core.git "$DIR/bats"
        export PATH=$DIR/bats/bin:$PATH
    fi

    if is_bin_in_path bats ; then
        echo "INFO: Finished Bats setup"
        return 0
    else
        echo "ERROR: Failed to clone and setup Bats"
        return 1
    fi

    echo ""
}


#------------------------------------------------------------------------------
# Clean files possibly still there after a previous execution
#------------------------------------------------------------------------------
clean() {

    rm -f ./Adder_testbench.sv
    rm -f files.f
    rm -f sim_main.cpp
}

#------------------------------------------------------------------------------
# Bats testsuite runner
#------------------------------------------------------------------------------
run_bats() {

    echo "INFO: Execute $1"
    echo ""

    bats "$DIR/$1.sh"
    ret=$?
    status=$((status + ret))
    [ "$ret" -ne 0 ] && echo -e "ERROR: $1 failed\n"
    return
}

#------------------------------------------------------------------------------
# Main function setting up the flow and launch Bats
#------------------------------------------------------------------------------
main () {

    echo ""
    echo "INFO: Start SVUT Regression"
    echo ""


    # Get script's location
    export DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
    export PATH="$DIR/..":$PATH

    # Remove dirties
    clean

    # Check Bats is in PATH, else clone it locally and push it in PATH
    setup_bats

    echo ""
    echo "INFO: Start Bats execution"
    echo ""

    # Execute all the testsuites
    run_bats "testsuite_create"
    run_bats "testsuite_run"
    run_bats "testsuite_run_args"
    run_bats "testsuite_examples"

    if [ $status -eq 0 ]; then
        echo "INFO: Regression finished successfully. SVUT sounds alive ^^"
        exit 0
    else
        echo "ERROR: Regression failed"
        exit 1
    fi
}

main "$@"
