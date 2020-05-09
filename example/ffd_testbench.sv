/// Mandatory file to be able to launch SVUT flow
`include "svut_h.sv"

/// Specify here the module to load or setup the path in files.f
`include "ffd.v"

`timescale 1 ns / 100 ps

module ffd_testbench();

    `SVUT_SETUP

    reg  aclk;
    reg  arstn;
    reg  d;
    reg  q;

    ffd
    dut
    (
    aclk,
    arstn,
    d,
    q
    );

    /// An example to create a clock for icarus:
    initial aclk = 0;
    always #2 aclk <= ~aclk;

    /// An example to dump data for visualization
    initial begin
        $dumpfile("waveform.vcd");
        $dumpvars(0, ffd_testbench);
    end

    task setup(msg="");
    begin
        /// setup() runs when a test begins
        arstn = 1'b0;
        d = 1'b0;
        #100;
        arstn = 1'b1;
    end
    endtask

    task teardown(msg="");
    begin
        /// teardown() runs when a test ends
    end
    endtask

    `TEST_SUITE("FIRST_ONE")

    ///    Available macros:"
    ///
    ///    - `INFO("message"):      Print a grey message
    ///    - `SUCCESS("message"):   Print a green message
    ///    - `WARNING("message"):   Print an orange message and increment warning counter
    ///    - `CRITICAL("message"):  Print an pink message and increment critical counter
    ///    - `ERROR("message"):     Print a red message and increment error counter
    ///
    ///    - `FAIL_IF(aSignal):                 Increment error counter if evaluaton is true
    ///    - `FAIL_IF_NOT(aSignal):             Increment error coutner if evaluation is false
    ///    - `FAIL_IF_EQUAL(aSignal, 23):       Increment error counter if evaluation is equal
    ///    - `FAIL_IF_NOT_EQUAL(aSignal, 45):   Increment error counter if evaluation is not equal
    ///    - `ASSERT(aSignal):                  Increment error counter if evaluation is not true
    ///    - `ASSERT((aSignal == 0)):           Increment error counter if evaluation is not true
    ///
    ///    Available flag:
    ///
    ///    - `LAST_STATUS: tied to 1 is last macro did experience a failure, else tied to 0

    `UNIT_TEST("CHECK RESET IS APPLIED")

        `INFO("I will test if q output is 0 after reset");
        # 10;
        `FAIL_IF(q, "this flip-flop should be zeroed after reset");
        `ASSERT(q===0, "this flip-flop should be zeroed after reset");

    `UNIT_TEST_END

    `UNIT_TEST("DRIVE THE FFD")

        `INFO("I will test if q output is 1 after d assertion");
        # 10;
        d = 1'b1;
        @ (posedge aclk);
        @ (posedge aclk);
        `FAIL_IF_NOT(q, "this flip-flop should be enabled after reset");
        `ASSERT(q===1, "this flip-flop should be enabled after reset");
        # 10;

    `UNIT_TEST_END

    `TEST_SUITE_END

endmodule
