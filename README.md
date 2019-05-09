# SystemVerilog Unit Test Flow (svut)

## Introduction

svut is a very simple flow to create a Verilog/SystemVerilog unit test.
It is widely inspired by [SVUnit](http://agilesoc.com/open-source-projects/svunit/),
but it's written in python and run with [Icarus Verilog](http://iverilog.icarus.com/).
svut follows KISS principle: [Keep It Simple, Stupid](https://en.wikipedia.org/wiki/KISS_principle).

Hope it can help you!

### How to install it

Git clone the repository in a path and setup your $PATH to call the scripts from anywhere:

    git clone git@githuh.com:damofthemoon/svut.git yourPath
    export PATH="yourPath":$PATH

For instance:

    git clone git@githuh.com:damofthemoon/svut.git $HOME/.svut
    export PATH=$HOME/.svut/:$PATH

### How to use it

To create a unit test of a verilog module, call the command:

    svutCreate your_file.v

svut will create "your_file_unit_test.sv" which contains your module
instanciated and a place to write your testcase(s).
To run a test, call the command:

    svutRun -test your_file_unit_test.sv

or simply

    svutRun

svut will scan your current folder, search for the files with "_unit_test.sv" suffix
and run all tests available.

Follow a example to use with a basic FFD. Copy/paste this basic FFD model in a file name ffd.v:

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

ffd_unit_tests.v has been dropped in the folder from you called svutCreate. It contains all you need
to start populating your testcases. In the header, you can include directly your DUT file by uncommenting
the line:

    // `include "ffd.v"

or you can store the path to your file into a 'files.f' file, automatically recognized by SVUT.
Right after the module instance, you can use the example to generate a clock (uncomment):

    initial aclk = 0;
    always #2 aclk <= ~aclk;

Next line explains how to dump your signals values into a VCD file to open a waveform in GTKWave:

    initial $dumpvars(0, ffd_unit_test);

Two functions follow, setup() and teardown(). setup() is called before each testcase execution,
tearndown() after each testcase execution. A testcase is enclosed between to specific defines:

    `UNIT_TEST(TESTNAME)
        ...
    `UNIT_TEST_END

TESTNAME has to be configured for each testcase. Then you can use the macros provided to display
information, warning, error and check some signals status and values. Each error found with macros
is counted and used to determine a testcase status.

To test the FFD, add the next line into setup() to drive the reset and start the FFD:

    arstn = 1'b0;
    d = 1'b0;
    #100;
    arstn = 1'b1;

and into the testcase:

    `FAIL_IF(q);

Here is a basic unit test checking if the FFD output is 0 after reset. You can play around to
test SVUT macros. Enjoy!

## External tools

To use `make gui` command, opening by default GTKwave, be sure to setup properly this tool in your path.
For Mac OS users, first install with brew:

    brew cask install gtkwave

Then setup your path:

    export PATH=/Applications/gtkwave.app/Contents/Resources/bin/:$PATH

You may need to install a Perl module, Switch. First enter in cpan (juste type cpan in your shell), then:

    install Switch

GTKWave should open up without problems :)

# TODO

    [ ] Add [Verilator](https://www.veripool.org/wiki/verilator) support
