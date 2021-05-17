#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
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
SOFTWARE.
"""

import os
import sys

if __name__ == '__main__':

    # Handle the input arguments. A file must be passed
    # and exists in file system
    file_name = ""

    if len(sys.argv) >= 1:
        file_name = sys.argv[1]
    else:
        print("ERROR: please specify a file to parse")
        sys.exit(1)

    if os.path.isfile(file_name):
        verilog = open(file_name, "r")
        print("INFO: Start to generate the template")
    else:
        print("ERROR: Can't find file %s to load..." % file_name)
        sys.exit(1)

    # The next section will parse the user file and extract the parameters
    # list, the IOs name and width and the module name. Expect Verilog 2005
    # style ONLY for IOs!
    # This FSM is a very basic parser and handle simple construction.
    # TODO: replace it with serious implementation like pyverilog

    # List of flags activated during parsing steps.
    intoComment = "No"
    inlineComment = "Yes"
    moduleFound = "No"
    parameterFound = "No"
    ioFound = "No"
    done = "No"

    instance = {"name": "", "io": [], "parameter": []}

    # One by one the loop will detect the different part of the
    # module declaration. Steps are:
    # 1. Detect block comments in file header
    # 2. Detect module name
    # 3. Detect parameters
    # 4. Detect input/output of the module
    # Once detected, store the result for testsuite writing

    for line in verilog:

        # Remove space at beginning and end of line
        line = line.strip()

        # Detect comment block in header and avoid to parse them
        # A block comment like a license is thus ignored
        if line[0:2] == "/*":
            intoComment = "Yes"
            inlineComment = "No"
        elif line[0:2] == "//":
            intoComment = "Yes"
            inlineComment = "Yes"
        elif line[0:2] == "*/" or line[-2:] == "*/":
            intoComment = "No"
            inlineComment = "No"

        if intoComment == "Yes":
            if inlineComment == "Yes":
                intoComment = "No"
            continue

        # Search for the module name if `module` found, split line with " " and
        # get the last part, the name.  Expect `module module_name` on the line
        if moduleFound == "No":
            if "module" in line:
                moduleFound = "Yes"
                info = line.split(" ")
                instance["name"] = info[1]
                if instance["name"][-1] == ";":
                    instance["name"] = instance["name"][:-1]

        # Search for the parameter if present search a line with `parameter`,
        # remove comment at the end of line, replace comma with semicolon and
        # store the line, ready to be written as a parameter declaration in
        # testsuite file
        if parameterFound == "No":
            if line[0:9] == "parameter":
                _line = line.split("//")[0].strip()
                _line = _line.replace("\t", " ")
                _line = _line.replace(",", "")
                if _line[-1] != ";":
                    _line = _line + ";"
                instance["parameter"].append(_line)

        # Search for input or ouput, change comma to semicolon, signed|wire to
        # reg and remove IO mode. Remove comment at the end of line
        # Ready to be written into testsuitefile.
        if ioFound == "No":
            if line[0:5] == "input" or line[0:6] == "output":
                _line = line.split("//")[0].strip()
                if line[0:10] == "input var ":
                    _line = _line.replace("input var", "")
                else:
                    _line = _line.replace("input", "")
                _line = _line.replace("output", "")
                _line = _line.replace("signed", "logic")
                _line = _line.replace("wire", "logic")
                _line = _line.replace("reg", "logic")
                _line = _line.replace(",", "")
                _line = _line + ";"
                instance["io"].append(_line.strip())

    # This section stores the testsuite file with information
    # extracted. Give also example to use the macro, create a clock,
    # dump signals in a waveform and skeleton of the testsuite.

    # print instance["parameter"]
    utfile = open(instance["name"] + "_testbench.sv", "w")

    utfile.write("/// Mandatory file to be able to launch SVUT flow\n")
    utfile.write("`include \"svut_h.sv\"\n\n")
    utfile.write("/// Specify the module to load or on files.f\n")
    utfile.write("""`include \"""" + file_name + """\"\n\n""")
    utfile.write("""`timescale 1 ns / 100 ps\n""")
    utfile.write("""\n""")
    utfile.write("""module """ + instance["name"] + "_testbench();\n")
    utfile.write("""\n""")
    utfile.write("""    `SVUT_SETUP\n""")
    utfile.write("""\n""")

    # Print parameter declaration if present
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
            # get left and right side around the equal sign
            _param = param.split("=")
            # split over space of the let side ('parameter param_name')
            _param = _param[-2].split(" ")
            # remove empty element in the list
            _param = list(filter(None, _param))
            # grab parameter name, always the last element in the list
            utfile.write("    " + _param[-1])
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
            # write until the semicolumn
            utfile.write("    " + _io[-1][:-1])
            if ix == len(instance["io"]) - 1:
                utfile.write("\n")
            else:
                utfile.write(",\n")

    utfile.write("""    );\n""")

    utfile.write("""\n""")
    utfile.write("""    // To create a clock:\n""")
    utfile.write("""    // initial aclk = 0;\n""")
    utfile.write("""    // always #2 aclk = ~aclk;\n""")
    utfile.write("""\n""")
    utfile.write("""    // To dump data for visualization:\n""")
    utfile.write("""    // initial begin\n""")
    utfile.write("""    //     $dumpfile("%s.vcd");\n""" % (instance["name"] + "_testbench"))
    utfile.write("""    //     $dumpvars(0, %s);\n""" % (instance["name"] + "_testbench"))
    utfile.write("""    // end\n""")
    utfile.write("""\n""")
    utfile.write("""    task setup(msg="");\n""")
    utfile.write("""    begin\n""")
    utfile.write("""        /// setup() runs when a test begins\n""")
    utfile.write("""    end\n""")
    utfile.write("""    endtask\n""")
    utfile.write("""\n""")
    utfile.write("""    task teardown(msg="");\n""")
    utfile.write("""    begin\n""")
    utfile.write("""        /// teardown() runs when a test ends\n""")
    utfile.write("""    end\n""")
    utfile.write("""    endtask\n""")
    utfile.write("""\n""")
    utfile.write("""    `TEST_SUITE("SUITE_NAME")\n""")
    utfile.write("""\n""")
    utfile.write("""    ///    Available macros:"\n""")
    utfile.write("""    ///\n""")
    utfile.write("""    ///    - `MSG("message"):       Print a raw white message\n""")
    utfile.write("""    ///    - `INFO("message"):      Print a blue message with INFO: prefix\n""")
    utfile.write("""    ///    - `SUCCESS("message"):   Print a green message if SUCCESS: prefix\n""")
    utfile.write("""    ///    - `WARNING("message"):   Print an orange message with WARNING: prefix and increment warning counter\n""")
    utfile.write("""    ///    - `CRITICAL("message"):  Print a purple message with CRITICAL: prefix and increment critical counter \n""")
    utfile.write("""    ///    - `ERROR("message"):     Print a red message with ERROR: prefix and increment error counter\n""")
    utfile.write("""    ///\n""")
    utfile.write("""    ///    - `FAIL_IF(aSignal):                 Increment error counter if evaluaton is true\n""")
    utfile.write("""    ///    - `FAIL_IF_NOT(aSignal):             Increment error coutner if evaluation is false\n""")
    utfile.write("""    ///    - `FAIL_IF_EQUAL(aSignal, 23):       Increment error counter if evaluation is equal\n""")
    utfile.write("""    ///    - `FAIL_IF_NOT_EQUAL(aSignal, 45):   Increment error counter if evaluation is not equal\n""")
    utfile.write("""    ///    - `ASSERT(aSignal):                  Increment error counter if evaluation is not true\n""")
    utfile.write("""    ///    - `ASSERT((aSignal == 0)):           Increment error counter if evaluation is not true\n""")
    utfile.write("""    ///\n""")
    utfile.write("""    ///    Available flag:\n""")
    utfile.write("""    ///\n""")
    utfile.write("""    ///    - `LAST_STATUS: tied to 1 is last macro did experience a failure, else tied to 0\n""")
    utfile.write("""\n""")
    utfile.write("""    `UNIT_TEST("TEST_NAME")\n""")
    utfile.write("""\n""")
    utfile.write("""        /// Describe here the testcase scenario\n""")
    utfile.write("""        /// \n""")
    utfile.write("""        /// Because SVUT uses long nested macros, it's possible\n""")
    utfile.write("""        /// some local variable declaration leads to compilation issue.\n""")
    utfile.write("""        /// You should declare your variables after the IOs declaration to avoid that.\n""")
    utfile.write("""\n""")
    utfile.write("""    `UNIT_TEST_END\n""")
    utfile.write("""\n""")
    utfile.write("""    `TEST_SUITE_END\n""")
    utfile.write("""\n""")
    utfile.write("""endmodule\n""")
    utfile.close()

    # After the file is written and ready to use, print some
    # recommandation to setup and call SVUT flow.
    print("")
    print("INFO: Unit test template for %s generated in: %s" % (instance["name"], instance["name"] + "_testbench.sv"))
    print("")
    print("      To launch SVUT, don't forget to setup its environment variable. For instance:")
    print("")
    print("      export SVUT=\"$HOME/.svut\"")
    print("      export PATH=$SVUT:$PATH")
    print("")
    print("      You can find a Makefile example to launch your unit test in your SVUT install folder")
    print("")
    print("      cp $SVUT/Makefile.example ./Makefile")
    print("")
    print("      Once copied, you can setup your fileset in files.f")
    print("")

    os.system("touch files.f")
