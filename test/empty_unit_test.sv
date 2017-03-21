`timescale 1 ns / 1 ps
`include "svut_h.sv"

module timeout_unit_test;

    `SVUT_SETUP

    task setup();
    begin
        // setup() runs when a test begins
    end
    endtask

    task teardown();
    begin
        // teardown() runs when a test ends
    end
    endtask

    `UNIT_TESTS

    `UNIT_TEST(TEST_SET_TIMEOUT)
    
    `UNIT_TEST_END

    `UNIT_TESTS_END

endmodule

