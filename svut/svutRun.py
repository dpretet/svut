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

# pylint: disable=W0621

import os
import sys
import argparse
import filecmp
import subprocess
import datetime
from timeit import default_timer as timer
from datetime import timedelta
from pathlib import Path, PosixPath

SCRIPTDIR = os.path.abspath(os.path.dirname(__file__))

def check_arguments(args):
    """
    Verify the arguments are correctly setup
    """

    if "iverilog" in args.simulator or "icarus" in args.simulator:
        print_event("Run with Icarus Verilog")
    elif "verilator" in args.simulator:
        print_event("Run with Verilator")
    else:
        print_event("ERROR: Simulator not supported")
        sys.exit(1)

    if not args.test:
        print_event("ERROR: No testcase or path to testcases passed")
        sys.exit(1)

    for path in args.test:
        error = False
        if not path.exists():
            error = True
            print_event("ERROR: %s does not exist" % path)

    if error:
        sys.exit()

    if args.compile_only and args.run_only:
        print("ERROR: Both compile-only and run-only are used")
        sys.exit(1)

    if (args.compile_only or args.run_only) and args.test=="all":
        print_event("ERROR: compile-only or run-only can't be used with multiple testbenchs")
        sys.exit(1)

    return 0


def check_tb_extension(test : PosixPath):
    """
    Check the extension to be sure it can be run
    """
    if test.suffix not in [".v",".sv"]:
        print("ERROR: Failed to find supported extension. Must use either *.v or *.sv")
        sys.exit(1)


def copy_svut_h():
    """
    First copy svut_h.sv macro in the user folder if not present or different
    """

    # Resolve first the real place h file is located
    # The place is different if the python is directly call or if
    # using the symlink
    org_hfile = SCRIPTDIR + "/svut/svut_h.sv"

    if not os.path.isfile(org_hfile):
        org_hfile =  SCRIPTDIR + "/svut_h.sv"

    curr_hfile = os.getcwd() + "/svut_h.sv"

    if (not os.path.isfile(curr_hfile)) or\
            (not filecmp.cmp(curr_hfile, org_hfile)):
        print("INFO: Copy up-to-date version of svut_h.sv")
        os.system("cp " + org_hfile + " " + os.getcwd())

    return 0


def find_unit_tests(test_dir : PosixPath):
    """
    Parse all unit test files of the current folder
    and return a list of available tests
    """

    supported_prefix = ["tb_", "ts_", "testbench_", "testsuite_", "unit_test_"]
    supported_suffix = ["_unit_test", "_testbench","_testsuite", "_tb", "_ts"]
    files = []

    # Parse the current folder
    for path in Path(test_dir).iterdir():
        # Check only the files
        if not path.is_file():
            continue

        # Files not ending with .sv or .v are skipped
        if path.suffix not in [".sv",".v"]:
            continue

        if path.stem.startswith(tuple(supported_prefix)):
            files.append(path)

        if path.stem.endswith(tuple(supported_suffix)):
            files.append(path)

    # Remove duplicated file if contains both prefix and suffix
    files = list(set(files))

    if not files:
        print("ERROR: Can't find tests to run")
        sys.exit(1)

    return files


def print_banner(tag):
    """
    A banner printed when the flow starts
    """
    print()
    print("""       ______    ____  ________""")
    print("""      / ___/ |  / / / / /_  __/""")
    print("""      \\__ \\| | / / / / / / /  """)
    print("""     ___/ /| |/ / /_/ / / /   """)
    print("""    /____/ |___/\\____/ /_/""")
    print()
    print(f"    {tag}")
    print()

    return 0

def helper(tag):
    """
    Help menu
    """

    print_banner(tag)
    print("    https://github.com/dpretet/svut")
    print()

    return 0


def get_defines(defines):
    """
    Return a string with the list of defines ready to drop in icarus
    """
    simdefs = ""

    if not defines:
        return simdefs

    defs = defines.split(';')

    for _def in defs:
        if _def:
            simdefs += "-D" + _def + " "

    return simdefs


def create_iverilog(args, test):
    """
    Create the Icarus Verilog command to launch the simulation
    """

    cmds = []

    if not os.path.isfile("svut.out"):
        print_event("Testbench executable not found. Will build it")
        args.run_only = False

    # Build testbench executable
    if not args.run_only:

        cmd = "iverilog -g2012 -Wall -o svut.out "

        if args.define:
            cmd += get_defines(args.define)

        if args.dotfile:

            dotfiles = ""

            for dot in args.dotfile:
                if os.path.isfile(dot):
                    dotfiles += dot + " "

            if dotfiles:
                cmd += "-f " + dotfiles + " "

        if args.include:
            incs = " ".join(args.include)
            cmd += "-I " + incs + " "

        cmd += test + " "
        cmds.append(cmd)

    # Execute testbench
    if not args.compile_only:

        cmd = "vvp "
        if args.vpi:
            cmd += args.vpi + " "

        cmd += "svut.out "
        cmds.append(cmd)

    return cmds


def create_verilator(args, test):
    """
    Create the Verilator command to launch the simulation
    """

    testname = os.path.basename(test).split(".")[0]

    cmds = []

    if not os.path.isfile("build/V" + testname + ".mk"):
        print_event("Testbench executable not found. Will build it")
        args.run_only = False


    # Build testbench executable
    if not args.run_only:

        cmd = """verilator -Wall --trace --Mdir build +1800-2012ext+sv """
        cmd += """+1800-2005ext+v -Wno-STMTDLY -Wno-UNUSED -Wno-UNDRIVEN -Wno-PINCONNECTEMPTY """
        cmd += """-Wpedantic -Wno-VARHIDDEN -Wno-lint """

        if args.define:
            cmd += get_defines(args.define)

        if args.dotfile:

            dotfiles = ""

            for dot in args.dotfile:
                if os.path.isfile(dot):
                    dotfiles += dot + " "

            if dotfiles:
                cmd += "-f " + dotfiles + " "

        if args.include:
            for inc in args.include:
                cmd += "+incdir+" + inc + " "

        cmd += "-cc --exe --build -j --top-module " + testname + " "
        cmd += test + " " + args.main
        cmds.append(cmd)

    # Execution command
    if not args.compile_only:
        cmd = "build/V" + testname
        cmds.append(cmd)

    return cmds


def print_event(event):
    """
    Print an event during SVUT execution
    TODO: manage severity/verbosity level
    """

    time = datetime.datetime.now().time().strftime('%H:%M:%S')

    print("SVUT (@ " + time + ") " + event, flush=True)
    print("")

    return 0


def get_git_tag():
    """
    Return current SVUT version
    """

    curr_path = os.getcwd()
    os.chdir(SCRIPTDIR)

    try:
        git_tag = subprocess.check_output(["git", "describe", "--tags", "--abbrev=0"])
        git_tag = git_tag.strip().decode('ascii')
    except subprocess.CalledProcessError as err:
        print("WARNING: Can't get last git tag. Will return v0.0.0")
        git_tag = "v0.0.0"

    os.chdir(curr_path)
    return git_tag

def get_test_dir(input: list) -> PosixPath:
    if len(input) == 1 and input[0].is_dir():
        return input[0]

    return None


def main():
    """
    Main function
    """

    parser = argparse.ArgumentParser(description='SystemVerilog Unit Test Flow')

    # SVUT options

    parser.add_argument('-sim', dest='simulator', type=str, default="icarus",
                        help='The simulator to use, icarus or verilator.')

    parser.add_argument('-test', dest='test', type=str, default=[os.getcwd()], nargs="*",
                        help='Unit test to run. A file,list of files or path to test files')

    parser.add_argument('-no-splash', dest='splash', default=False, action='store_true',
                        help='Don\'t print the banner when executing')

    parser.add_argument('-version', dest='version', action='store_true',
                        default="", help='Print version menu')

    # Simulator options

    parser.add_argument('-f', dest='dotfile', type=str, default=["files.f"], nargs="*",
                        help="A dot file (*.f) with incdir, define and file path")

    parser.add_argument('-include', dest='include', type=str, nargs="*",
                        default="", help='Specify an include folder; can be used along a dotfile')

    parser.add_argument('-main', dest='main', type=str, default="sim_main.cpp",
                        help='Verilator main cpp file, like sim_main.cpp')

    parser.add_argument('-define', dest='define', type=str, default="",
                        help='''A list of define separated by ; \
                            ex: -define "DEF1=2;DEF2;DEF3=3"''')

    parser.add_argument('-vpi', dest='vpi', type=str, default="",
                        help='''A string of arguments passed as is to Icarus (only), separated \
                                by a space ex: -vpi "-M. -mMyVPI"''')

    # SVUT Execution options

    parser.add_argument('-run-only', dest='run_only', default=False, action='store_true',
                        help='Only run existing executable but build it if not present')

    parser.add_argument('-compile-only', dest='compile_only', default=False, action='store_true',
                        help='Only prepare the testbench executable')

    parser.add_argument('-dry-run', dest='dry', default=False, action='store_true',
                        help='Just print the command, don\'t execute')


    args = parser.parse_args()
    args.test = [Path(x) for x in args.test]

    git_tag = get_git_tag()

    if args.version:
        helper(git_tag)
        sys.exit(0)

    if not args.splash:
        print_banner(git_tag)

    # Lower the simulator name to ease checking
    args.simulator = args.simulator.lower()

    # Check arguments consistency
    check_arguments(args)

    # If the user specifies a directory to look for files, test_dir will point to this directory
    # If the user does not specify any test files or directy at all, test_dir will point to the CWD
    # If the user specifies one or more test files, test_dir is none and no searching will take place
    test_dir = get_test_dir(args.test)
    if test_dir:
        args.test = find_unit_tests(test_dir)

    # Copy svut_h.sv if not present or not up-to-date
    copy_svut_h()

    cmdret = 0

    start = timer()

    test : PosixPath
    for test in args.test:

        check_tb_extension(test)

        if "iverilog" in args.simulator or "icarus" in args.simulator:
            cmds = create_iverilog(args, str(test))

        elif "verilator" in args.simulator:
            cmds = create_verilator(args, str(test))

        print_event("Start " + test.name)

        # Execute commands one by one
        for cmd in cmds:

            print_event(cmd)

            if not args.dry:
                if os.system(cmd):
                    cmdret += 1
                    print("ERROR: Command failed: " + cmd)
                    break

        print_event("Stop " + test.name)

    end = timer()
    print_event("Elapsed time: " + str(timedelta(seconds=end-start)))
    print()

    sys.exit(cmdret)

if __name__ == '__main__':
    main()
