#include "build/Vffd_unit_test.h"
#include "verilated.h"

// Current simulation time (64-bit unsigned)
vluint64_t main_time = 0;
// Called by $time in Verilog
double sc_time_stamp() {
    return main_time;
}

int main(int argc, char** argv, char** env) {

    // Verilator must compute traced signals
    Verilated::traceEverOn(true);
    // Pass application arguments to Verilator
    Verilated::commandArgs(argc, argv);
    // Create an object with the unit test file
    Vffd_unit_test* top = new Vffd_unit_test;
    // Initialize SVUT built-in clock and active-low reset
    top->svut_aclk = 0;
    top->svut_arstn = 0;
    // Wait for the end of the testbench
    while (!Verilated::gotFinish()) {
        // Increment main_time
        main_time++;
        // Assert reset at the very beginning
        if (!top->svut_aclk) {
            if (main_time < 10) {
                top->svut_arstn = 0;  // Assert reset
            } else {
                top->svut_arstn = 1;  // Deassert reset
            }
        }
        top->svut_aclk = !top->svut_aclk;
        top->eval();
    }
    // Delete object and exit
    delete top;
    exit(0);
}
