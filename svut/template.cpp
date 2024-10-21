#include "build/V${name}_testbench.h"
#include "verilated.h"
// To uncomment if use FST format
// #include "verilated_fst_c.h"


int main(int argc, char** argv, char** env) {

    // To uncomment if use FST format
    // Initialize trace object for FST
    // VerilatedFstC* tfp = new VerilatedFstC;

    // Construct a VerilatedContext to hold simulation time, etc.
    // Multiple modules (made later below with Vtop) may share the same
    // context to share time, or modules may have different contexts if
    // they should be independent from each other.
    // Using unique_ptr is similar to
    // "VerilatedContext* contextp = new VerilatedContext" then deleting at end.
    const std::unique_ptr<VerilatedContext> contextp{new VerilatedContext};
    // Set debug level, 0 is off, 9 is highest presently used
    // May be overridden by commandArgs argument parsing
    contextp->debug(0);
    // Verilator must compute traced signals
    contextp->traceEverOn(true);
    // Pass arguments so Verilated code can see them, e.g. $value$plusargs
    // This needs to be called before you create any model
    Verilated::commandArgs(argc, argv);
    V${name}_testbench* top = new V${name}_testbench;

    // To uncomment if use FST format
    // Attach FST trace to the model
    // top->trace(tfp, 99);  // Depth of 99 levels
    // tfp->open("waveform.fst");  // Open FST file

    // Simulate until $$finish()
    while (!Verilated::gotFinish()) {
        // Evaluate model;
        top->eval();
    }

    // Final model cleanup
    top->final();
    // To uncomment if use FST format
    // tfp->close();  // Close the FST file

    // Destroy model
    delete top;

    // Return good completion status
    return 0;
}
