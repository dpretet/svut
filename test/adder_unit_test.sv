`timescale 1 ns / 1 ps
`include "svut_h.sv"
`include "adder.v"

module adder_unit_test;

    `SVUT_SETUP

    parameter LATENCY = 0;
    parameter WIDTH = 32;

    reg              aclk;
    reg              arstn;
    reg              srst;
    reg  [WIDTH-1:0] a;
    reg  [WIDTH-1:0] b;
    wire [WIDTH-1:0] c;

    adder 
    #(
    LATENCY,
    WIDTH
    )
    dut 
    (
    aclk,
    arstn,
    srst,
    a,
    b,
    c
    );

    // initial aclk = 0;
    // always #2 aclk <= ~aclk;

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

    `UNIT_TEST(TESTNAME)
        #100;
        $display("RUNNING");
    `UNIT_TEST_END

    `UNIT_TESTS_END

endmodule

