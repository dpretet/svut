test_run_wrong_run_compile_only() { #@test

    run "$DIR/../svutRun.py" "-run-only" "-compile-only"
    [ "$status" -eq 1 ]
}

test_run_all_with_run_only() { #@test

    run "$DIR/../svutRun.py" "-run-only"
    [ "$status" -eq 1 ]
}

test_run_all_with_compile_only() { #@test

    run "$DIR/../svutRun.py" "-compile-only"
    [ "$status" -eq 1 ]
}

test_run_wrong_simulator() { #@test

    run "$DIR/../svutRun.py" "-sim" "xxx"
    [ "$status" -eq 1 ]
}

test_run_version() { #@test

    run "$DIR/../svutRun.py" "-version"
    [ "$status" -eq 0 ]
}

test_run_no_tb_present_to_scan() { #@test

    run "$DIR/../svutRun.py" "-test" "../"
    [ "$status" -eq 1 ]
}

test_run_not_a_tb_path() { #@test

    run "$DIR/../svutRun.py" "-test" "../example/"
    [ "$status" -eq 1 ]
}

test_run_dry_run() { #@test

    run "$DIR/../svutRun.py" "-test" "../example/ffd_testbench.sv" "-dry-run"
    [ "$status" -eq 0 ]
}
