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

    svutRun your_file_unit_test.sv

or simply
    
    svutRun

svut will scan your current folder, search for the files with "_unit_test.sv" suffix
and run all tests available.

Enjoy!

PS: [Verilator](https://www.veripool.org/wiki/verilator) simulator is planned soon, as QuestaSim

PS: To use make gui command, opening by default GTKwave, be sure to setup properly this tool in your path.
    For Mac OS users, first install with brew:

    brew cask install gtkwave

Then setup your path:

    export PATH=/Applications/gtkwave.app/Contents/Resources/bin/:$PATH

You may need to install a Perl module, Switch. First enter in cpan (juste type cpan in your shell), then:

    install Switch

GTKWave should open up without problems :)
