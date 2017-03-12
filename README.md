# SystemVerilog Unit Test Flow

## Introduction

svut is a very simple system to create a Verilog/SystemVerilog unit test.
It is widely inspired by [SVUnit](http://agilesoc.com/open-source-projects/svunit/), 
but it's written in python and can run [Icarus Verilog](http://iverilog.icarus.com/) 
and [Verilator] (https://www.veripool.org/wiki/verilator) as simulator.
svut follows KISS principle: [Keep It Simple, Stupid](https://en.wikipedia.org/wiki/KISS_principle)

Hope it can help you!

### How to install it

Git clone the repository in a path:

    git clone git@githuh.com:ThotIp/svut.git yourPath

And setup your $PATH to call the scripts from anywhere:
    
    export PATH="yourPath":$PATH

### How to use it

To create a unit test of a verilog module, call the command:

    ./svutCreate your_file.v

svut will create "your_file_unit_test.sv" which contains your module
instanciated and a place to write your testcase(s). It copies along
your new module svut_h.v, containing some macros to use in your test.

To run a test, call the command:

    ./svutRun your_file_unit_test.sv

or simply
    
    ./svutRun

svut will scan your current folder, search for the files with "_unit_test.sv"
and run the tests.

Enjoy!

