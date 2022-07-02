test_run_ffd_example_icarus() { #@test

    run bash -c "cd ../example && "$DIR/../svutRun" -test ffd_testbench.sv -sim icarus"
    [ "$status" -eq 0 ]
}

test_run_ffd_example_verilator_failure() { #@test

    run bash -c "cd ../example && "$DIR/../svutRun" -test ffd_testbench.sv -sim verilator"
    [ "$status" -eq 1 ]
}
