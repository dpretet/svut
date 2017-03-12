#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" ThotIP Unit Test generator v1.0

Usage:
  svutCreate.py <name> [--space] [--verbose]
  svutCreate.py (-h | --help)
  svutCreate.py --version

Options:
  <name>        The file name
  --space       To specify the space identation. tab or a number
  --verbose     Print info for debug purpose   
  -h --help     Show this screen.
  --version     Show version.


"""

from docopt import docopt

if __name__ == '__main__':

    """

    x - Use a file as argument
        x - Read the module name
        x - Read the parameter and store them
        x - Read the signal, input and output and store them
        x - Inline declaration only
    x - Write the timescale
    x - Write the include of the file to test
    x - Write the macros include
    x - Write the signal list
    x    - reg for input
    x    - wire for output
    x - Write the instance with implicit declaration
    x - Write the setup() and teardown() functions
    x - Write the test parts of the testcase
    x - Write endmodule


    """

    arguments = docopt(__doc__, version='ThotIP Unit Test generator v1.0')

    if arguments["--verbose"]:
        print(arguments)

    verilog = open(arguments["<name>"], "r")

    moduleFound = "No"
    parameterFound = "No"
    ioFound = "No"
    done = "No"

    io = []
    instance = {"name" : None, "io" : [], "parameter" : []}

    for line in verilog:

        # Remove space at beginning and end of line
        line = line.strip()

        # Search for the module name
        if moduleFound == "No":
            if "module" in line:
                moduleFound = "Yes"
                info = line.split(" ")
                instance["name"] = info[1]
                if instance["name"][-1] == ";":
                    instance["name"] = instance["name"][:-1]

        # Search for the parameter if present
        if parameterFound == "No":
            if line[0:9] == "parameter":
                _line = line.replace(",", ";")
                if _line[-1] != ";":
                    _line = _line + ";"
                instance["parameter"].append(_line)

        # Search for the input and output
        if ioFound == "No":

            if line[0:5] == "input":
                _line = line.replace("wire", "reg ")
                _line = _line.replace(",", ";")
                _line = _line.replace("input", "")
                instance["io"].append(_line.strip())

            if line[0:6] == "output":
                _line = line.replace(",", ";")
                _line = _line.replace("output", "")
                if _line[-1] != ";":
                    _line = _line + ";"
                instance["io"].append(_line.strip())

            #parameterFound = "Yes"
            #ioFound = "Yes"

    if arguments["--verbose"]:
        print "INFO: information extracted:"
        print instance


    utname = arguments["<name>"] + "_unit_test"

    utfile = open(instance["name"]+"_unit_test.sv", "w")

    utfile.write("""`timescale 1 ns / 1 ps\n""")
    utfile.write("`include \"unit_test_h.sv\"\n")
    utfile.write("""`include \"""" + arguments["<name>"]  + """\"\n""")
    utfile.write("""\n""")
    utfile.write("""module """ + instance["name"] + "_unit_test;\n")
    utfile.write("""\n""")
    utfile.write("""    string name = \"%s\";\n""" % instance["name"]+"_unit_test")
    utfile.write("""\n""")
    
    # Print parameter declarationif present
    if instance["parameter"]:
        for param in instance["parameter"]:
            utfile.write("""    """ + param + "\n")
        utfile.write("""\n""")

    # Print input/output declaration if present
    if instance["io"]:
        for io in instance["io"]:
            utfile.write("""    """ + io + "\n")
        utfile.write("""\n""")
    
    # Write the instance
    utfile.write("""    """ + instance["name"] + " \n")
    
    # Print parameter instance if present
    if instance["parameter"]:
        utfile.write("""    #(\n""")

        for ix, param in enumerate(instance["parameter"]):
            _param = param.split(" ")
            utfile.write("    " + _param[-3])
            if ix == len(instance["parameter"]) - 1:
                utfile.write("\n")
            else:
                utfile.write(",\n")
            
        utfile.write("    )\n")
    
    utfile.write("""    dut \n    (\n""")
    
    # Print input/output instance if present
    if instance["io"]:
        for ix, io in enumerate(instance["io"]):
            _io = io.split(" ")
            utfile.write("    " + _io[-1][:-1])
            if ix == len(instance["io"]) - 1:
                utfile.write("\n")
            else:
                utfile.write(",\n")
    
    utfile.write("""    );\n""")

    utfile.write("""\n""")
    utfile.write("""    // always #2 aclk <= ~aclk;\n""")
    utfile.write("""\n""")
    utfile.write("""    task setup();\n""")
    utfile.write("""        // setup() runs when a test begins\n""")
    utfile.write("""    endtask\n""")
    utfile.write("""\n""")
    utfile.write("""    task teardown();\n""")
    utfile.write("""        // teardown() runs when a test ends\n""")
    utfile.write("""    endtask\n""")
    utfile.write("""\n""")
    utfile.write("""    `UNIT_TESTS\n""")
    utfile.write("""\n""")
    utfile.write("""    `UNIT_TEST("test name")\n""")
    utfile.write("""        // Describe here your testcase\n""")
    utfile.write("""    `UNIT_TEST_END\n""")
    utfile.write("""\n""")
    utfile.write("""    `UNIT_TESTS_END\n""")
    utfile.write("""\n""")
    utfile.write("""endmodule\n""")
    utfile.write("""\n""")
    utfile.close()

