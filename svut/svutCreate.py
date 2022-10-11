#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright 2022 The SVUT Authors

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

# pylint: disable=C0103

import os
import sys
import re
from string import Template
from pathlib import Path

SCRIPTDIR = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))

def parse_verilog(verilog):

    """
    The next section will parse the user file and extract the parameters
    list, the IOs name and width and the module name. Expect Verilog 2005
    style ONLY for IOs!
    This FSM is a very basic parser and handle simple construction.
    TODO: replace it with serious implementation like pyverilog
    """

    print("INFO: Extract information from module to test")

    # List of flags activated during parsing steps.
    intoComment = "No"
    inlineComment = "Yes"
    moduleFound = "No"
    parameterFound = "No"
    ioFound = "No"

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
                    _line = re.sub("input var", "", _line)
                else:
                    _line = re.sub("input", "", _line)
                _line = re.sub("output", "", _line)
                _line = re.sub("signed", "logic", _line)
                _line = re.sub("wire", "logic", _line)
                _line = re.sub("\sreg\s", "logic", _line)
                _line = re.sub(",", "", _line)
                _line = _line + ";"
                instance["io"].append(_line.strip())

    return instance


def get_instance(instance):
    """
    This functions creates the wires declaration and the module instance
    """

    print("INFO: Prepare the testbench")

    mod_inst = ""

    # Print parameter declaration if present
    if instance["parameter"]:
        for param in instance["parameter"]:
            mod_inst += """    """ + param + "\n"
        mod_inst += """\n"""

    # Print input/output declaration if present
    if instance["io"]:
        for io in instance["io"]:
            mod_inst += """    """ + io + "\n"
        mod_inst += """\n"""

    # Write the instance
    mod_inst += """    """ + instance["name"] + " \n"

    # Print parameter instance if present
    if instance["parameter"]:

        mod_inst += """    #(\n"""

        # First get the longest name
        maxlen = 0
        for _, param in enumerate(instance["parameter"]):

            _param = param.split(" ")
            _name = _param[-3]

            if len(_name) > maxlen:
                maxlen = len(_name)

        for ix, param in enumerate(instance["parameter"]):
            # get left and right side around the equal sign
            _param = param.split("=")
            # split over space of the let side ('parameter param_name')
            _param = _param[-2].split(" ")
            # remove empty element in the list
            _param = list(filter(None, _param))
            # grab parameter name, always the last element in the list
            _name = _param[-1]

            _text = "    ." + _name + \
                " " * (maxlen - len(_name)) + \
                " (" + _name + ")"

            mod_inst += _text
            if ix == len(instance["parameter"]) - 1:
                mod_inst += "\n"
            else:
                mod_inst += ",\n"

        mod_inst += "    )\n"

    mod_inst += """    dut \n    (\n"""

    # Print input/output instance if present
    if instance["io"]:

        # First get the longest name
        maxlen = 0
        for _, ios in enumerate(instance["io"]):
            _io = ios.split(" ")
            _name = _io[-1][:-1]
            if len(_name) > maxlen:
                maxlen = len(_name)

        for ix, io in enumerate(instance["io"]):

            _io = io.split(" ")
            # write until the semicolumn
            _name = _io[-1][:-1]

            _text = "    ." + _name + \
                " " * (maxlen - len(_name)) + \
                " (" + _name + ")"

            mod_inst += _text
            if ix == len(instance["io"]) - 1:
                mod_inst += "\n"
            else:
                mod_inst += ",\n"

    mod_inst += """    );\n"""

    return mod_inst

def dump_template(file_name, tmpl):
    """
    Store the template transformated after substitution
    """
    try:
        # Store the testbench
        with open(file_name, "w", encoding="utf-8") as ofile:
            ofile.write(tmpl)
            ofile.close()
    except OSError:
        print("Can't store template")
        sys.exit(1)

    return 0


def print_recommandation(name):
    """
    After the file is written and ready to use, print some
    recommandation to setup and call SVUT flow.
    """

    print("")
    print(f"INFO: Testbench for {name} has been generated in: {name}_testbench.sv")
    print("")
    print("      To launch SVUT, don't forget to setup its environment variable. For instance:")
    print("")
    print("      export SVUT=\"$HOME/.svut\"")
    print("      export PATH=$SVUT:$PATH")
    print("")
    print("      The testbench needs to be tuned to generate clock, reset and test scenarios")
    print("")
    print("      You can setup your fileset in files.f")
    print("")
    print("      Then call SVUT with:")
    print("      svutRun -test my_testbench.sv -define \"DEF1=1;DEF2;DEF3=3\"")
    print("")
    print("      Further information can be found in Github:")
    print("      https://github.com/dpretet/svut#tutorial")
    print("")


def main():
    # Handle the input arguments. A file must be passed
    # and exists in file system
    FILE_NAME = ""

    if len(sys.argv) > 1:
        FILE_NAME = sys.argv[1]
    else:
        print("ERROR: please specify a file to parse")
        sys.exit(1)

    print("INFO: Start to generate the testbench")

    # First extract information from the module to test
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as verilog_module:
            verilog_info = parse_verilog(verilog_module)
    except OSError:
        print(f"ERROR: Can't find file {FILE_NAME} to load...")
        sys.exit(1)

    # Put in shape the module instance and the wire declarations
    module_inst = get_instance(verilog_info)
    # Setup the data to substitute in the template
    tmpl_data = dict(name=verilog_info["name"], module_inst=module_inst)

    # Load the system verilog template and substitute
    tmpl = Path(SCRIPTDIR+"/template.sv", encoding="utf-8").read_text()
    tmpl = Template(tmpl).substitute(tmpl_data)
    dump_template(verilog_info["name"] + "_testbench.sv", tmpl)

    # Load the cpp template and substitute
    tmpl = Path(SCRIPTDIR+"/template.cpp", encoding="utf-8").read_text()
    tmpl = Template(tmpl).substitute(tmpl_data)
    dump_template("sim_main.cpp", tmpl)

    # Print recommandation to users before exiting
    print_recommandation(verilog_info["name"])

    # Create a files.f if doesn't exist, else preserve the existing
    os.system("touch files.f")

    sys.exit(0)

if __name__ == '__main__':
    main()

