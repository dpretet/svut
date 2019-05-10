// Mandatory file to be able to launch SVUT flow
`include "svut_h.sv"

// Specify here the module to load or setup the path in files.f
`include "ffd.v"

`timescale 1 ns / 1 ps

module ffd_unit_test;

    `SVUT_SETUP

    reg  aclk;
    reg  arstn;
    reg  d;
    wire q;

    ffd
    dut
    (
    aclk,
    arstn,
    d,
    q
    );

    // An example to create a clock
    initial aclk = 0;
    always #2 aclk <= ~aclk;

    // An example to dump data for visualization
    initial $dumpvars(0, ffd_unit_test);

    task setup();
    begin
        arstn = 1'b0;
        d = 1'b0;
        #100;
        arstn = 1'b1;
    end
    endtask

    task teardown();
    begin
        // teardown() runs when a test ends
    end
    endtask

    `UNIT_TESTS

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

    `UNIT_TEST(TEST_IF_RESET_IS_APPLIED_WELL)

        `INFO("Start TEST_IF_RESET_IS_APPLIED_WELL");

            `FAIL_IF(q);

        `INFO("Test finished");

    `UNIT_TEST_END

    `UNIT_TESTS_END

endmodule

