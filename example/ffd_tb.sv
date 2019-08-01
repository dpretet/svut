/* Alternate version of the FFD test that uses a "test bench"
 * suffix and newer macros that let you name tests and test 
 * suites. Also uses ASSERT-style macros instead of the 
 * FAIL_IF-style for those coming from prior unit test 
 * frameworks such as JUnit or Python's unittest.
 * 
 * See the comments in svut_h.sv for a full list of changes.
 */
 
 // Mandatory file to be able to launch SVUT flow
`include "svut_h.sv"

// Specify here the module to load or setup the path in files.f
`include "ffd.v"

`timescale 1 ns / 1 ps

module ffd_tb;

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

    // WAS: UNIT_TEST
    `TEST_SUITE("ffd_tb")

        /* Available macros:

               - `INFO("message"); Print a grey message
               - `SUCCESS("message"); Print a green message
               - `WARNING("message"); Print an orange message and increment warning counter
               - `CRITICAL("message"); Print an pink message and increment critical counter
               - `ERROR("message"); Print a red message and increment error counter

               - `FAIL_IF(aSignal); Increment error counter if evaluaton is positive
               - `ASSERT(aSignal, [reason]); Same as FAIL_IF, reason string is optional
               - `FAIL_IF_NOT(aSignal); Increment error coutner if evaluation is false
               - `FAIL_IF_EQUAL(aSignal, 23); Increment error counter if evaluation is equal
               - `FAIL_IF_NOT_EQUAL(aSignal, 45); Increment error counter if evaluation is not equal
               - `ASSERT_EQUAL(aSignal, value, [reason]); Same as FAIL_IF_NOT_EQUAL, with optional reason
        */

        /* Available flag:

               - `LAST_STATUS: tied to 1 is last macros has been asserted, else tied to 0
        */

    // WAS: UNIT_TEST
    `NAMED_TEST("Test if reset is applied well")

            `ASSERT(q);

    `NAMED_TEST_END

    `TEST_SUITE_END

endmodule

