# SystemVerilog Unit Test (SVUT)

[![GitHub license](https://img.shields.io/github/license/damofthemoon/svut)](https://github.com/damofthemoon/svut/blob/master/LICENSE)
[![Build Status](https://travis-ci.org/damofthemoon/svut.svg?branch=master)](https://travis-ci.org/damofthemoon/svut)
[![GitHub issues](https://img.shields.io/github/issues/damofthemoon/svut)](https://github.com/damofthemoon/svut/issues)
[![GitHub stars](https://img.shields.io/github/stars/damofthemoon/svut)](https://github.com/damofthemoon/svut/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/damofthemoon/svut)](https://github.com/damofthemoon/svut/network)
[![Twitter](https://img.shields.io/twitter/url/https/github.com/damofthemoon/svut?style=social)](https://twitter.com/intent/tweet?text=Wow:&url=https%3A%2F%2Fgithub.com%2Fdamofthemoon%2Fsvut)


## Introduction

SVUT is a very simple flow to create a Verilog/SystemVerilog unit test.  It is
widely inspired by [SVUnit](http://agilesoc.com/open-source-projects/svunit/),
but it's written in python and run with [Icarus
Verilog](http://iverilog.icarus.com/). SVUT follows KISS principle: [Keep It
Simple, Stupid](https://en.wikipedia.org/wiki/KISS_principle).

Hope it can help you!

### How to install it

Git clone the repository in a path. Set up the SVUT environment variable
and add SVUT to `$PATH`:

```bash
    git clone git@github.com:damofthemoon/svut.git $HOME/.svut
    export SVUT=$HOME/.svut
    export PATH=$SVUT:$PATH
```

SVUT relies on [Icarus Verilog](http://iverilog.icarus.com/) as simulation
back-end.  Please install it with your favourite package manager and be sure to
use a version greater or equal to v10.2. SVUT is tested with `v10.2` and cannot
work with with lower version (`<= v9.x`). SVUT  can also relies on
[Verilator](https://www.veripool.org/wiki/verilator). As for Icarus, please
install it with your package manager and be sure to use a recent version. SVUT
is tested with Verilator `v4.0.30`.


### How to use it


To create a unit test of a verilog module, call the command:

```bash
    svutCreate your_file.v
```

SVUT will create "your_file_unit_test.sv" which contains your module
instanciated and a place to write your testcase(s). Some codes are also commented
to describe the different macros and how to create a clock or dump a VCD for GTKWave.
To run a test, call the command:

```bash
    svutRun -test your_file_unit_test.sv
```

or simply

```bash
    svutRun
```

SVUT will scan your current folder, search for the files with "_unit_test.sv" suffix
and run all tests available.

# Example

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

ffd_unit_test.v has been dropped in the folder from you called svutCreate. It contains all you need
to start populating your testcases. In the header, you can include directly your DUT file (uncomment):

```verilog
    `include "ffd.v"
```

or you can store the path to your file into a `files.f` file, automatically recognized by SVUT.
Populate it with the files describing your IP. You can also specify include folder in this way:

```bash
    +incdir+$HOME/path/to/include/
```

Right after the module instance, you can use the example to generate a clock (uncomment):

```verilog
    initial aclk = 0;
    always #2 aclk <= ~aclk;
```

Next line explains how to dump your signals values into a VCD file to open a
waveform in GTKWave (uncomment):

```verilog
    initial $dumpvars(0, ffd_unit_test);
```

Two functions follow, setup() and teardown(). Use them to configure the
environment of the testcases:
- setup() is called before each testcase execution
- tearndown() after each testcase execution

A testcase is enclosed between to specific defines:

```verilog
    `UNIT_TEST("TESTNAME")
        ...
    `UNIT_TEST_END
```

TESTNAME is a string (optional), which will be displayed when test execution
will start Then you can use the macros provided to display information,
warning, error and check some signals status and values. Each error found with
macros increments an error counter which determine a testcase status. If the
error counter is bigger than 0, the test is considered as failed.

A testsuite, comprising several `UNIT_TEST` is declared with another define:

```verilog
    `TEST_SUITE("SUITENAME")
    ...

    `TEST_SUITE_END
```

To test the FFD, add the next line into setup() to drive the reset and init the FFD input:

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

Here is a basic unit test checking if the FFD output is 0 after reset. Once called `svutRun` in your
shell, you should see something similar:

```
    INFO:     Testsuite execution started

    INFO:     [100] Start TEST_IF_RESET_IS_APPLIED_WELL
    INFO:     [100] Test finished
    SUCCESS:  [100] Test successful

    INFO:     Testsuite execution finished @ 100

          -> STATUS:    1 /    1 test(s) passed
```

Now you know the basics of SVUT. The \*_unit_test.sv provides prototypes of available macros.
Try them and play around to test SVUT. You can find these files into the example folder.
A simple makefile.example is present at the root level of this repo to launch the flow. It contains
two targets, `make test` and `make gui`. Enjoy!

## External tools

To use `make gui` command, opening by default GTKwave, be sure to setup properly this tool in your path.
For Mac OS users, first install with brew:

```bash
    brew cask install gtkwave
```

Then setup your path to launch `gtkwave` from your shell (restart it)

```bash
    export PATH="/Applications/gtkwave.app/Contents/Resources/bin/":$PATH
```

You may need to install a Perl module, Switch. First enter in cpan (juste type cpan in your shell,
or sudo cpan), then:

```bash
    install Switch
```

GTKWave should open up without problems :)


## License

Copyright 2020 The SVUT Authors

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
associated documentation files (the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge, publish, distribute,
sublicense, and/or sell copies of the Software, and to permit persons to whom the Software
is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial
portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
imitations under the License.
