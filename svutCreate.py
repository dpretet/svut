#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright 2017 Damien Pretet ThotIP

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

import os, sys, argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='ThotIP Unit test runner v1.0')

    parser.add_argument('--verbose', dest='verbose', type=str, default=0,
                                        help='Activate verbose mode')

    parser.add_argument('--name', dest='name', type=str, default=None, nargs="*",
                                        help="The verilog module to load")

    args = parser.parse_args()

    args.name = args.name[0]
    if os.path.isfile(args.name):
        verilog = open(args.name, "r")
    else:
        print "ERROR: Can't find file %s to load..." % args.name
        sys.exit(1)

    moduleFound = "No"
    parameterFound = "No"
    ioFound = "No"
    done = "No"

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

    if args.verbose:
        print "INFO: information extracted:"
        print instance


    utname = args.name + "_unit_test"

    utfile = open(instance["name"]+"_unit_test.sv", "w")

    utfile.write("""`timescale 1 ns / 1 ps\n""")
    utfile.write("`include \"svut_h.sv\"\n")
    utfile.write("""`include \"""" + args.name  + """\"\n""")
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
    utfile.write("""    // always #2 aclk <= ~aclk;\n""")
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
    utfile.write("""    `UNIT_TESTS\n""")
    utfile.write("""\n""")
    utfile.write("""    `UNIT_TEST(TESTNAME)\n""")
    utfile.write("""        // Describe here your testcase\n""")
    utfile.write("""    `UNIT_TEST_END\n""")
    utfile.write("""\n""")
    utfile.write("""    `UNIT_TESTS_END\n""")
    utfile.write("""\n""")
    utfile.write("""endmodule\n""")
    utfile.write("""\n""")
    utfile.close()

    curdir  = os.path.dirname(os.path.abspath(__file__))
    os.system("cp %s ." % (curdir+"/svut_h.sv"))

