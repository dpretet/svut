test_run_wrong_run_compile_only() { #@test

    run "$DIR/../svut/svutRun.py" "-run-only" "-compile-only"
    [ "$status" -eq 1 ]
}

test_run_all_with_run_only() { #@test

    run "$DIR/../svut/svutRun.py" "-run-only"
    [ "$status" -eq 1 ]
}

test_run_all_with_compile_only() { #@test

    run "$DIR/../svut/svutRun.py" "-compile-only"
    [ "$status" -eq 1 ]
}

test_run_wrong_simulator() { #@test

    run "$DIR/../svut/svutRun.py" "-sim" "xxx"
    [ "$status" -eq 1 ]
}

test_run_version() { #@test

    run "$DIR/../svut/svutRun.py" "-version"
    [ "$status" -eq 0 ]
}

test_run_no_tb_present_to_scan() { #@test

    run "$DIR/../svut/svutRun.py" "-test" "../"
    [ "$status" -eq 1 ]
}

test_run_not_a_tb_path() { #@test

    run "$DIR/../svut/svutRun.py" "-test" "../example/"
    [ "$status" -eq 1 ]
}

test_run_no_tests() { #@test

    run "cd" "-" "&&" "./svutRun"
    [ "$status" -eq 1 ]
}


test_run_dry_run() { #@test

    run "$DIR/../svut/svutRun.py" "-test" "../example/ffd_testbench.sv" "-dry-run"
    [ "$status" -eq 0 ]
}
