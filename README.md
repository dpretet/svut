# SystemVerilog Unit Test (SVUT)

[![GitHub license](https://img.shields.io/github/license/dpretet/svut)](https://github.com/dpretet/svut/blob/master/LICENSE)
![Github Actions](https://github.com/dpretet/svut/actions/workflows/ci_ubuntu.yaml/badge.svg)
![Github Actions](https://github.com/dpretet/svut/actions/workflows/ci_macos.yaml/badge.svg)
[![GitHub issues](https://img.shields.io/github/issues/dpretet/svut)](https://github.com/dpretet/svut/issues)
[![GitHub stars](https://img.shields.io/github/stars/dpretet/svut)](https://github.com/dpretet/svut/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/dpretet/svut)](https://github.com/dpretet/svut/network)
[![Twitter](https://img.shields.io/twitter/url/https/github.com/dpretet/svut?style=social)](https://twitter.com/intent/tweet?text=Wow:&url=https%3A%2F%2Fgithub.com%2Fdpretet%2Fsvut)


## Introduction

SVUT is a very simple flow to create a Verilog/SystemVerilog unit test.  It is
widely inspired by [SVUnit](http://agilesoc.com/open-source-projects/svunit/),
but it's written in python and run with [Icarus
Verilog](http://iverilog.icarus.com/). SVUT follows KISS principle: [Keep It
Simple, Stupid](https://en.wikipedia.org/wiki/KISS_principle).

Hope it can help you!

### How to Install

#### Pypi

SVUT is availble on Pypi and can be installed as following:

```bash
pip3 install svut
```

#### Git

Git clone the repository in a path. Set up the SVUT environment variable
and add SVUT to `$PATH`:

```bash
export SVUT=$HOME/.svut
git clone https://github.com/dpretet/svut.git $SVUT
export PATH=$SVUT:$PATH
```

SVUT relies on [Icarus Verilog](http://iverilog.icarus.com/) as simulation
back-end.  Please install it with your favourite package manager and be sure to
use a version greater or equal to v10.2. SVUT is tested with `v10.2` and cannot
work with with lower version (`<= v9.x`).

SVUT can also use [Verilator](https://github.com/verilator/verilator) but the support
is more limited for the moment. A future release will fix that. An example to understand
how to use it along Icarus can be found [here](https://github.com/dpretet/friscv/tree/master/test/common)


### How to use it


To create a unit test of a verilog module, call the command:

```bash
svutCreate your_file.v
```

No argument is required. SVUT will create "your_file_testbench.sv" which contains your module
instanciated and a place to write your testcase(s). Some codes are also commented to describe the
different macros and how to create a clock or dump a VCD for GTKWave. To run a test, call the
command:

```bash
svutRun -test your_file_testbench.sv
```

or simply `svutRun` to execute all testbenchs in the current folder.

```bash
svutRun
```

SVUT will scan your current folder, search for the files with "\_testbench.sv"
suffix and run all tests available. Multiple suffix patterns are [possible](https://github.com/dpretet/svut/blob/master/svutRun.py#L46).

svutRun proposes several arguments, most optional:

- `-test`: specify the testsuite file path or a folder containing tests
- `-f`: pass the fileset description, default is `files.f`
- `-sim`: specify the simulator, `icarus` or `verilator`
- `-main`: specify the main.cpp file when using verilator, default is `sim_main.cpp`
- `-define`: pass verilog defines to the tool, like `-define "DEF1=2;DEF2;DEF3=3"`
- `-vpi`: specify a compiled VPI, for instance `-vpi "-M. -mMyVPI"`
- `-dry-run`: print the commands but don't execute them
- `-include`: to pass include path, several can be passed like `-include folder1 folder2`
- `-no-splash`: don't print SVUT splash banner, printed by default
- `-compile-only`: just compile the testbench, don't execute it
- `-run-only`: just execute the testbench, if no executable found, also build it


# Tutorial

Copy/paste this basic FFD model in a file named ffd.v into a new folder:

```verilog
`timescale 1 ns / 1 ps

module ffd
    (
    input  wire aclk,
    input  wire arstn,
    input  wire d,
    output reg  q
    );

    always @ (posedge aclk or negedge arstn) begin
        if (arstn == 1'b0) q <= 1'b0;
        else q <= d;
    end

endmodule
```

Then run:

```bash
svutCreate ffd.v
```

ffd_testbench.v has been dropped in the folder from you called svutCreate. It
contains all you need to start populating your testcases. In the header, you
can include directly your DUT file (uncomment):

```verilog
`include "ffd.v"
```

or you can store the path to your file into a `files.f` file, automatically
recognized by SVUT. Populate it with the files describing your IP. You can
also specify include folder in this way:

```bash
+incdir+$HOME/path/to/include/
```

Right after the module instance, you can use the example to generate a clock
(uncomment):

```verilog
initial aclk = 0;
always #2 aclk <= ~aclk;
```

Next line explains how to dump your signals values into a VCD file to open a
waveform in GTKWave (uncomment):

```verilog
initial $dumpvars(0, ffd_unit_test);
initial $dumpfile("ffd_testbench.vcd");
```

Two functions follow, `setup()` and `teardown()`. Use them to configure the
environment of the testcases:
- setup() is called before each testcase execution
- teandown() after each testcase execution

A testcase is enclosed between to specific defines:

```verilog
`UNIT_TEST("TESTNAME")
    ...
`UNIT_TEST_END
```

TESTNAME is a string (optional), which will be displayed when test execution
will start. Then you can use the macros provided to display information,
warning, error and check some signals status and values. Each error found with
macros increments an error counter which determine a testcase status. If the
error counter is bigger than 0, the test is considered as failed.

A testsuite, comprising several `UNIT_TEST` is declared with another define:

```verilog
`TEST_SUITE("SUITENAME")
    ...
`TEST_SUITE_END
```

To test the FFD, add the next line into `setup()` to drive the reset and init the
FFD input:

```verilog
arstn = 1'b0;
d = 1'b0;
#100;
arstn = 1'b1;
```

and into the testcase:

```verilog
`FAIL_IF(q);
```

Here is a basic unit test checking if the FFD output is 0 after reset. Once
called `svutRun` in your shell, you should see something similar:

```
INFO: Start testsuite << FFD Testsuite >> (@ 0)

INFO: Starting << Test 0: Check reset is applied >> (@ 0)
I will test if Q output is 0 after reset (@ 100000)
SUCCESS: Test 0 pass (@ 110000)

INFO: Starting << Test 1: Drive the FFD >> (@ 110000)
I will test if Q output is 1 after D assertion (@ 210000)
SUCCESS: Test 1 pass (@ 236000)

INFO: Stop testsuite 'FFD Testsuite' (@ 236000)
  - Warning number:  0
  - Critical number: 0
  - Error number:    0
  - STATUS: 2/2 test(s) passed
```

SVUT relies (optionally) on files.f to declare fileset and define. The user
can also choose to pass define in the command line:

```bash
svutRun -test my_testbench.sv -define "DEF1=1;DEF2;DEF3=3"
```

SVUT doesn't check possible collision between define passed in command line
and the others defined in files.f. Double check that point if unexpected
behavior occurs during testbench.

Finally, SVUT supports VPI for Icarus. Follow an example to compile and set up
the flow of an hypothetic UART, compiled with iverilog and using a define "PORT":

```bash
iverilog-vpi uart.c
svutRun -vpi "-M. -muart" -define "PORT=3333" -t ./my_testbench.sv &
```

Now you know the basics of SVUT. The generated testbench provides prototypes of
available macros. Try them and play around to test SVUT. You can find these
files into the example folder.

Enjoy!


## License

Copyright 2021 The SVUT Authors

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.  imitations under the License.
