// Mandatory file to be able to launch SVUT flow
`include "svut_h.sv"

// Specify here the module to load or setup the path in files.f
`include "Adder.v"

`timescale 1 ns / 1 ps

module Adder_unit_test_OK;

    `SVUT_SETUP

    parameter WIDTH = 8;

    reg             aclk;
    reg             arstn;
    reg             clr;
    reg             inc;
    reg [WIDTH-1:0] out;

    Adder
    #(
    WIDTH
    )
    dut
    (
    aclk,
    arstn,
    clr,
    inc,
    out
    );

    // An example to create a clock
    initial aclk = 0;
    always #2 aclk <= ~aclk;

    // An example to dump data for visualization
    initial $dumpvars(0, Adder_unit_test_OK);

    task setup(msg="Here is the setup function");
    begin
        // setup() runs when a test begins
        inc = 1'b0;
        clr = 1'b0;
        arstn = 1'b0;
        #100;
        arstn = 1'b1;
    end
    endtask

    task teardown(msg="Here is the teardown function");
    begin
        // teardown() runs when a test ends
    end
    endtask

    `TEST_SUITE("This is my OK Testsuite")

        /* Available macros:

               - `INFO("message"); Print a grey message
               - `SUCCESS("message"); Print a green message
               - `WARNING("message"); Print an orange message and increment warning counter
               - `CRITICAL("message"); Print an pink message and increment critical counter
               - `ERROR("message"); Print a red message and increment error counter
               - `FAIL_IF(aSignal); Increment error counter if evaluaton is positive
               - `FAIL_IF_NOT(aSignal); Increment error coutner if evaluation is false
               - `FAIL_IF_EQUAL(aSignal, 23); Increment error counter if evaluation is equal
               - `FAIL_IF_NOT_EQUAL(aSignal, 45); Increment error counter if evaluation is not equal
        */

        /* Available flag:

               - `LAST_STATUS: tied to 1 is last macros has been asserted, else tied to 0
        */

    `UNIT_TEST("Macro test")

        `MSG("I print a message for myself in the future");
        `SUCCESS("All tests are expected OK!");
        // Basic tests of the main functions. All results are expected OK
        `INFO("Test FAIL_IF");
        `FAIL_IF(inc);
        `INFO("Test FAIL_IF_EQUAL");
        `FAIL_IF_EQUAL(out, 8'd18);
        `INFO("Test FAIL_IF_NOT_EQUAL");
        `FAIL_IF_NOT_EQUAL(out, 8'd0);
        @(posedge aclk);
        inc = 1'b1;
        `INFO("Test FAIL_IF_NOT");
        `FAIL_IF_NOT(inc);
        @(posedge aclk);
        inc = 1'b0;
        `INFO("Test FAIL_IF");
        `FAIL_IF(inc);
        `INFO("Test FAIL_IF_EQUAL");
        `FAIL_IF_EQUAL(out, 8'd0);
        `INFO("Test FAIL_IF_NOT_EQUAL");
        `FAIL_IF_NOT_EQUAL(out, 8'd1);

        `SUCCESS("Test finished");

    `UNIT_TEST_END

    `UNIT_TEST("Define check")

        `ifndef MYDEF1
            `ERROR("No define 1 found!");
        `endif

        if (`MYDEF1!=5)
            `ERROR("MYDEF1 is not equal to 5");

        `ifndef MYDEF2
            `ERROR("No define 2 found!");
        `endif

    `UNIT_TEST_END

    `TEST_SUITE_END

endmodule

