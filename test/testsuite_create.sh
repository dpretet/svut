test_create_adder_testbench() { #@test

    run "$DIR/../svutCreate" "$DIR/Adder.v"

    [ "$status" -eq 0 ]
    [ -e "Adder_testbench.sv" ]
    [ -e "sim_main.cpp" ]
    [ -e "files.f" ]

}


test_create_no_path() { #@test
    run "$DIR/../svutCreate"
    [ "$status" -eq 1 ]
}


test_create_bad_input_path() { #@test
    run "$DIR/../svutCreate" "$DIR/Add__er.v"
    [ "$status" -eq 1 ]
}
