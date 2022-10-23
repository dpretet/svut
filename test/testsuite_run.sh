test_run_ok_testsuite() { #@test

    run ../svutRun -test "$DIR/Adder_OK_testsuite.sv" -define "MYDEF1=5;MYDEF2"
    [ "$status" -eq 0 ]
}

test_run_ok_testsuite_failure() { #@test

    run ../svutRun -test "$DIR/Adder_OK_testsuite.sv"
    [ "$status" -eq 1 ]
}


test_run_ko_testsuite() { #@test

    run ../svutRun -test "$DIR/Adder_KO_testsuite.sv"
    [ "$status" -eq 0 ]
}

test_run_ko_testsuite_error_count() { #@test

    run exe_ko_to_log
    error_num=9
    [ $(grep -c "ERROR:" log) -eq "$error_num" ]
}

test_run_ko_testsuite_error_count_failure() { #@test

    run exe_ko_to_log
    error_num=0
    [ $(grep -c "ERROR:" log) -ne "$error_num" ]
}

function exe_ko_to_log() {
    ../svutRun -test "$DIR/Adder_KO_testsuite.sv" | tee log
}
