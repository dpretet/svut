# SystemVerilog Unit Test (SVUT)

## Introduction

svut is a very simple flow to create a Verilog/SystemVerilog unit test.
It is widely inspired by [SVUnit](http://agilesoc.com/open-source-projects/svunit/),
but it's written in python and run with [Icarus Verilog](http://iverilog.icarus.com/).
svut follows KISS principle: [Keep It Simple, Stupid](https://en.wikipedia.org/wiki/KISS_principle).

Hope it can help you!

### How to install it

Git clone the repository in a path and setup your $PATH to call the scripts from
anywhere. For instance:

    git clone git@githuh.com:damofthemoon/svut.git $HOME/.svut
    export PATH=$HOME/.svut/:$PATH

### How to use it

To create a unit test of a verilog module, call the command:

    svutCreate your_file.v

svut will create "your_file_unit_test.sv" which contains your module
instanciated and a place to write your testcase(s). Some codes are also commented
to describe the different macros and how to create a clock or dump a VCD for GTKWave.
To run a test, call the command:

    svutRun -test your_file_unit_test.sv

or simply

    svutRun

svut will scan your current folder, search for the files with "_unit_test.sv" suffix
and run all tests available.

# Example

Copy/paste this basic FFD model in a file named ffd.v into a new folder:

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

Then run:

    svutCreate ffd.v

ffd_unit_test.v has been dropped in the folder from you called svutCreate. It contains all you need
to start populating your testcases. In the header, you can include directly your DUT file (uncomment):

    `include "ffd.v"

or you can store the path to your file into a `files.f` file, automatically recognized by SVUT.
Populate it with the files describing your IP. You can also specify include folder in this way:

    +incdir+$HOME/path/to/include/

Right after the module instance, you can use the example to generate a clock (uncomment):

    initial aclk = 0;
    always #2 aclk <= ~aclk;

Next line explains how to dump your signals values into a VCD file to open a waveform in GTKWave (uncomment):

    initial $dumpvars(0, ffd_unit_test);

Two functions follow, setup() and teardown(). Use them to configure the environment of the testcases:
- setup() is called before each testcase execution
- tearndown() after each testcase execution

A testcase is enclosed between to specific defines:

    `UNIT_TEST(TESTNAME)
        ...
    `UNIT_TEST_END

TESTNAME has to be setup for each testcase, without space, capital letters or not.
Then you can use the macros provided to display information, warning, error and check some signals
status and values. Each error found with macros increments an error counter which determine a
testcase status. If the error counter is bigger than 0, the test is considered as failed.

To test the FFD, add the next line into setup() to drive the reset and init the FFD input:

    arstn = 1'b0;
    d = 1'b0;
    #100;
    arstn = 1'b1;

and into the testcase:

    `FAIL_IF(q);

Here is a basic unit test checking if the FFD output is 0 after reset. Once called `svutRun` in your
shell, you should see something similar:

    INFO:     Testsuite execution started

    INFO:     [100] Start TEST_IF_RESET_IS_APPLIED_WELL
    INFO:     [100] Test finished
    SUCCESS:  [100] Test successful

    INFO:     Testsuite execution finished @ 100

          -> STATUS:    1 /    1 test(s) passed

Now you know the basics of SVUT. The \*_unit_test.sv provides prototypes of available macros.
Try them and play around to test SVUT. You can find these files into the example folder.
A simple makefile.example is present at the root level of this repo to launch the flow. It contains
two targets, `make test` and `make gui`. Enjoy!

## External tools

To use `make gui` command, opening by default GTKwave, be sure to setup properly this tool in your path.
For Mac OS users, first install with brew:

    brew cask install gtkwave

Then setup your path to launch `gtkwave` from your shell (restart it)
    export PATH=/Applications/gtkwave.app/Contents/Resources/bin/:$PATH

You may need to install a Perl module, Switch. First enter in cpan (juste type cpan in your shell,
or sudo cpan), then:

    install Switch

GTKWave should open up without problems :)

# TODO

- [ ] Add [Verilator](https://www.veripool.org/wiki/verilator) support
