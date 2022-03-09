#!/usr/bin/env bash


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
    rm -fr bats
}


#------------------------------------------------------------------------------
# Main function setting up the flow and launch Bats
#------------------------------------------------------------------------------
main () {

    echo ""
    echo "INFO: Start SVUT Regresion"
    echo ""

    # Global status, the global return code
    status=0

    # Get script's location
    export DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

    # Remove dirties
    clean

    # First check Bats is in PATH, else clone it locally and push it in PATH
    setup_bats

    echo ""
    echo "INFO: Start Basts execution"
    echo ""

    bats "$DIR/testsuite_create.sh"
    ret=$?
    status=$((status + ret))
    [ "$ret" -eq 1 ] && echo "ERROR: testsuite_create failed"

    bats "$DIR/testsuite_run.sh"
    ret=$?
    status=$((status + ret))
    [ "$ret" -eq 1 ] && echo "ERROR: testsuite_run failed"

    if [ $status -eq 0 ]; then
        echo "INFO: Regression finished successfully. SVUT sounds alive ^^"
        exit 0
    else
        echo "ERROR: Regression failed"
        exit 1
    fi
}

main "$@"
