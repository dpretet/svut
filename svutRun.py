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

import os
import sys
import argparse

CURDIR = os.path.abspath(os.path.dirname(__file__))

"""
TODO:
* support verilator
* support questasim
"""


def find_unit_tests():
    """
    Parse all unit test files of the current folder
    """
    files = []
    # Parse the current folder
    for _file in os.listdir(os.getcwd()):
        # Check only the files
        if os.path.isfile(_file):
            # Ensure its at least a verilog file
            if _file.endswith("unit_test.sv") or _file.endswith("unit_test.v"):
                files.append(_file)
    return files


def create_iverilog(args, test):
    """
    Create the Icarus Verilog command to launch the simulation
    """
    cmds = []
    cmd = "iverilog -g2012 "

    if args.dotfile:
        dotfiles = " ".join(args.dotfile)
        cmd += "-f " + dotfiles + " "

    if args.include:
        incs = " ".join(args.include)
        cmd += "-I " + incs + " "

    cmd += test + " "

    # Check the extension and extract test name
    if test[-2:] != ".v" and test[-3:] != ".sv":
        print ("ERROR: failed to find supported for the unit test. Must a Verilog (.v) or SystemVerilog file (*.sv)")
        return 1

    cmds.append(cmd)

    cmd = "vvp a.out "
    if args.gui:
        cmd += "-lxt;"
    cmds.append(cmd)

    if args.gui:
        if os.path.isfile("wave.gtkw"):
            cmds.append("gtkwave *.lxt wave.gtkw &")
        else:
            cmds.append("gtkwave *.lxt &")

    return cmds


def create_verilator(args):
    """
    Create the Verilator command to launch the simulation
    """

    cmd = ""
    return cmd


def create_questasim(args):
    """
    Create the Questasim command to launch the simulation
    """

    cmd = "vlib work; "
    return cmd


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='ThotIP Unit test runner v1.0')

    parser.add_argument('-test', dest='test', type=str, default="all", nargs="*",
                        help='Unit test to run. Can be a file or a list of files')

    parser.add_argument('-f', dest='dotfile', type=str, default=None, nargs="*",
                        help="A dot file (file.f) to load with incdir, define and fileset")

    parser.add_argument('-sim', dest='simulator', type=str,
                        default="icarus",
                        help='The simulator to use. Can be Icarus Verilog, Verilator or Questasim')

    parser.add_argument('-gui', dest='gui',
                        action='store_true',
                        help='Active the lxt dump and open GTKWave when simulation ends')

    parser.add_argument('-dry-run', dest='dry',
                        action='store_true',
                        help='Just print the command, don\'t execute')

    parser.add_argument('-I', dest='include', type=str, nargs="*",
                        default="", help='An include folder')

    args = parser.parse_args()

    if isinstance(args.test, basestring):
        if "all" in args.test.lower():
            args.test = find_unit_tests()

    for tests in args.test:
        # Lower the simulator name to ease process
        args.simulator = args.simulator.lower()

        if "iverilog" in args.simulator or "icarus" in args.simulator:
            cmds = create_iverilog(args, tests, )

        elif "modelsim" in args.simulator or "questa" in args.simulator:
            cmds = create_questasim(args, tests)

        # Execute command on creation success
        if cmds != 1:
            # First copy macro in the user folder
            os.system("cp " + CURDIR + "/svut_h.sv " + os.getcwd())
            for cmd in cmds:
                if args.dry:
                    cmdret = 0
                    print(cmd)
                else:
                    cmdret = os.system(cmd)
                if cmdret:
                    print "ERROR: testsuite execution failed"
                    break
            os.system("rm -f " + os.getcwd() + "/svut_h.sv")
            sys.exit(cmdret)
        else:
            print ("ERROR: Command creation failed...")
            sys.exit(1)
