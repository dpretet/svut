/// Copyright 2024 The SVUT Authors
///
/// Permission is hereby granted, free of charge, to any person obtaining a copy
/// of this software and associated documentation files (the "Software"), to
/// deal in the Software without restriction, including without limitation the
/// rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
/// sell copies of the Software, and to permit persons to whom the Software is
/// furnished to do so, subject to the following conditions:
///
/// The above copyright notice and this permission notice shall be included in
/// all copies or substantial portions of the Software.
///
/// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
/// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
/// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
/// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
/// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
/// FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
/// IN THE SOFTWARE.

// Mandatory file to be able to launch SVUT flow
`include "svut_h.sv"
// Specify the module to load or on files.f
`include "ffd.sv"

`timescale 1 ns / 1 ps

module ffd_testbench();

    `SVUT_SETUP

    logic aclk;
    logic arstn;
    logic d;
    logic q;

    ffd
    dut
    (
    .aclk  (aclk),
    .arstn (arstn),
    .d     (d),
    .q     (q)
    );


    // An example to create a clock for icarus:
    initial aclk = 0;
    always #2 aclk <= ~aclk;

    // An example to dump data for visualization
    initial begin
        $dumpfile("waveform.vcd");
        $dumpvars(0, ffd_testbench);
    end

    task setup(msg="");
    begin
        // setup() runs when a test begins
        arstn = 1'b0;
        d = 1'b0;
        #100;
        arstn = 1'b1;
    end
    endtask

    task teardown(msg="");
    begin
        // teardown() runs when a test ends
    end
    endtask

    `TEST_SUITE("FFD Testsuite")

    //    Available macros:"
    //
    //    - `INFO("message"):      Print a grey message
    //    - `SUCCESS("message"):   Print a green message
    //    - `WARNING("message"):   Print an orange message and increment warning counter
    //    - `CRITICAL("message"):  Print an pink message and increment critical counter
    //    - `ERROR("message"):     Print a red message and increment error counter
    //
    //    - `FAIL_IF(aSignal):                 Increment error counter if evaluaton is true
    //    - `FAIL_IF_NOT(aSignal):             Increment error coutner if evaluation is false
    //    - `FAIL_IF_EQUAL(aSignal, 23):       Increment error counter if evaluation is equal
    //    - `FAIL_IF_NOT_EQUAL(aSignal, 45):   Increment error counter if evaluation is not equal
    //    - `ASSERT(aSignal):                  Increment error counter if evaluation is not true
    //    - `ASSERT((aSignal == 0)):           Increment error counter if evaluation is not true
    //
    //    Available flag:
    //
    //    - `LAST_STATUS: tied to 1 if last macro did experience a failure, else tied to 0

    `UNIT_TEST("Check reset is applied")

        `MSG("I will test if Q output is 0 after reset");
        # 10;
        `FAIL_IF(q, "this flip-flop should be zeroed after reset");
        `ASSERT(q===0, "this flip-flop should be zeroed after reset");

    `UNIT_TEST_END

    `UNIT_TEST("Drive the FFD")

        `MSG("I will test if Q output is 1 after D assertion");
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
