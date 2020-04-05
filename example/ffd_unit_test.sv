// Mandatory file to be able to launch SVUT flow
`include "svut_h.sv"

// Specify here the module to load or setup the path in files.f
`include "ffd.v"

`timescale 1 ns / 1 ps

module ffd_unit_test(input wire svut_aclk, svut_arstn);

    `SVUT_SETUP

    wire aclk;
    var arstn;
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

    // An example to dump data for visualization
    initial begin
        $dumpfile("waveform.vcd");
        $dumpvars(0, ffd_unit_test);
    end

    // An example to create a clock for icarus verilog:
    // initial aclk = 0;
    // initial arstn = 0;
    // always #2 aclk <= ~aclk;
    
    // Example to grab clock/reset generated with Verilator C++
    assign aclk = svut_aclk;
    // assign arstn = svut_arstn;
    integer i = 0;

    task setup();
    begin
        @ (posedge svut_aclk);
        i = 0;
        assign arstn = 1'b0;
        d = 1'b0;
        while (i<5) begin
            i++;
        end
        assign arstn = 1'b1;
    end
    endtask

    task teardown();
    begin
        // teardown() runs when a test ends
    end
    endtask

    /// Available macros:
    ///
    ///     - `INFO("message"); Print a grey message
    ///     - `SUCCESS("message"); Print a green message
    ///     - `WARNING("message"); Print an orange message and increment 
    ///       warning counter
    ///     - `CRITICAL("message"); Print an pink message and increment 
    ///       critical counter
    ///     - `ERROR("message"); Print a red message and increment error 
    ///       counter
    ///     - `FAIL_IF(aSignal); Increment error counter if evaluaton is 
    ///       positive
    ///     - `FAIL_IF_NOT(aSignal); Increment error coutner if evaluation 
    ///       is false
    ///     - `FAIL_IF_EQUAL(aSignal, 23); Increment error counter if 
    ///       evaluation is equal
    ///     - `FAIL_IF_NOT_EQUAL(aSignal, 45); Increment error counter if 
    ///       evaluation is not equal
    ///
    ///    Available flag:
    ///
    ///     - `LAST_STATUS: tied to 1 is last macros did experienced 
    ///       a failure, else tied to 0

    `TEST_SUITE("RESET TestSuite")

    `UNIT_TEST("IS_RESET_WELL_APPPLIED")

        `INFO("I will test if q output is 0 after reset");
        `FAIL_IF(q);
        `INFO("q is 0 after reset!");

    `UNIT_TEST_END

    `TEST_SUITE_END

endmodule
