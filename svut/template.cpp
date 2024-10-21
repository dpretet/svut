#include "build/V${name}_testbench.h"
#include "verilated.h"
// Uncomment if use FST format
// #include "verilated_fst_c.h"

int main(int argc, char** argv, char** env) {

    // Uncomment if use FST format
    // VerilatedFstC* tfp = new VerilatedFstC;

    Verilated::commandArgs(argc, argv);
    V${name}_testbench* top = new V${name}_testbench;

    // Uncomment if use FST format
    // top->trace(tfp, 99);  // Depth of 99 levels
    // tfp->open("waveform.fst");  // Open FST file

    // Simulate until $$finish()
    while (!Verilated::gotFinish()) {

        // Evaluate model;
        top->eval();
    }

    // Final model cleanup
    top->final();
    // Uncomment if use FST format
    // tfp->close();  // Close the FST file

    // Destroy model
    delete top;

    // Return good completion status
    return 0;
}
