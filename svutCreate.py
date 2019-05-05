#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright 2019 Damien Pretet

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import os
import sys

if __name__ == '__main__':

    file_name = ""

    if len(sys.argv) >= 1:
        file_name = sys.argv[1]
    else:
        print "ERROR: please specify a file to parse"
        sys.exit(1)

    if os.path.isfile(file_name):
        verilog = open(file_name, "r")
        print "INFO: Start to generate the template"
    else:
        print "ERROR: Can't find file %s to load..." % file_name
        sys.exit(1)

    intoComment = "No"
    moduleFound = "No"
    parameterFound = "No"
    ioFound = "No"
    done = "No"

    instance = {"name": "", "io": [], "parameter": []}

    for line in verilog:

        # Remove space at beginning and end of line
        line = line.strip()

        # Detect comment block and avoid to parse them
        if line[0:1] == "/*":
            intoComment = "Yes"
        elif line[0:1] == "*/" or line[-2:] == "*/":
            intoComment = "No"

        if intoComment == "Yes":
            continue

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
                _line = line.split("//")[0].strip()
                _line = _line.replace("\t", " ")
                _line = _line.replace(",", ";")
                if _line[-1] != ";":
                    _line = _line + ";"
                instance["parameter"].append(_line)

        # Search for the input and output
        if ioFound == "No":

            if line[0:5] == "input":
                _line = line.split("//")[0].strip()
                _line = _line.replace("signed", "reg")
                _line = _line.replace("wire", "reg ")
                _line = _line.replace(",", ";")
                _line = _line.replace("input", "")
                instance["io"].append(_line.strip())

            if line[0:6] == "output":

                _line = line.split("//")[0].strip()
                _line = _line.replace(",", ";")
                _line = _line.replace("signed", "wire")
                _line = _line.replace("output", "")
                if _line[-1] != ";":
                    _line = _line + ";"
                instance["io"].append(_line.strip())

    # print "INFO: information extracted:"
    # print instance

    utname = file_name + "_unit_test"

    utfile = open(instance["name"] + "_unit_test.sv", "w")

    utfile.write("// Mandatory file to be able to launch SVUT flow\n")
    utfile.write("`include \"svut_h.sv\"\n\n")
    utfile.write("// Specify here the module to load or setup the path in files.f\n")
    utfile.write("""//`include \"""" + file_name + """\"\n\n""")
    utfile.write("""`timescale 1 ns / 1 ps\n""")
    utfile.write("""\n""")
    utfile.write("""module """ + instance["name"] + "_unit_test;\n")
    utfile.write("""\n""")
    utfile.write("""    `SVUT_SETUP\n""")
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
    utfile.write("""    // An example to create a clock\n""")
    utfile.write("""    // initial aclk = 0;\n""")
    utfile.write("""    // always #2 aclk <= ~aclk;\n""")
    utfile.write("""\n""")
    utfile.write("""    // An example to dump data for visualization\n""")
    utfile.write("""    // initial $dumpvars(0, %s);\n""" % (instance["name"] + "_unit_test"))
    utfile.write("""\n""")
    utfile.write("""    task setup();\n""")
    utfile.write("""    begin\n""")
    utfile.write("""        // setup() runs when a test begins\n""")
    utfile.write("""    end\n""")
    utfile.write("""    endtask\n""")
    utfile.write("""\n""")
    utfile.write("""    task teardown();\n""")
    utfile.write("""    begin\n""")
    utfile.write("""        // teardown() runs when a test ends\n""")
    utfile.write("""    end\n""")
    utfile.write("""    endtask\n""")
    utfile.write("""\n""")
    utfile.write("""    `UNIT_TESTS\n\n""")
    utfile.write("""        /* Available macros:\n\n""")
    utfile.write("""               - `INFO("message"); Print a grey message\n""")
    utfile.write("""               - `SUCCESS("message"); Print a green message\n""")
    utfile.write("""               - `WARNING("message"); Print an orange message and increment warning counter\n""")
    utfile.write("""               - `CRITICAL("message"); Print an pink message and increment critical counter\n""")
    utfile.write("""               - `ERROR("message"); Print a red message and increment error counter\n""")
    utfile.write("""               - `FAIL_IF(aSignal); Increment error counter if evaluaton is positive\n""")
    utfile.write("""               - `FAIL_IF_NOT(aSignal); Increment error coutner if evaluation is false\n""")
    utfile.write("""               - `FAIL_IF_EQUAL(aSignal, 23); Increment error counter if evaluation is equal\n""")
    utfile.write("""               - `FAIL_IF_NOT_EQUAL(aSignal, 45); Increment error counter if evaluation is not equal\n""")
    utfile.write("""        */\n\n""")
    utfile.write("""        /* Available flag:\n\n""")
    utfile.write("""               - `LAST_STATUS: tied to 1 is last macros has been asserted, else tied to 0 \n""")
    utfile.write("""        */\n\n""")
    utfile.write("""    `UNIT_TEST(TESTNAME)\n""")
    utfile.write("""\n""")
    utfile.write("""        `INFO("Start TESTNAME");\n""")
    utfile.write("""\n""")
    utfile.write("""        // Describe here the testcase scenario\n""")
    utfile.write("""\n""")
    utfile.write("""        `INFO("Test finished");\n""")
    utfile.write("""\n""")
    utfile.write("""    `UNIT_TEST_END\n""")
    utfile.write("""\n""")
    utfile.write("""    `UNIT_TESTS_END\n""")
    utfile.write("""\n""")
    utfile.write("""endmodule\n""")
    utfile.write("""\n""")
    utfile.close()

    print ""
    print "INFO: Unit test template for %s generated in: %s" % (instance["name"], instance["name"] + "_unit_test.sv")
    print ""
    print "      To launch SVUT, don't forget to setup its environment variable. For instance:"
    print ""
    print "      export SVUT=\"HOME/.svut\""
    print "      export PATH=$SVUT:$PATH"
    print ""
    print "      You can find a Makefile example to launch your unit test in your SVUT install folder"
    print ""
    print "      cp $SVUT/Makefile.example ./Makefile"
    print ""
    print "      Once copied, you can setup your fileset in files.f"
    print ""

    os.system("touch files.f")
