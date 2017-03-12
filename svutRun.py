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

import sys
import argparse

"""
* find all files
* build the command for icarus
* write the macros
* support verilator
"""

def create_iverilog(args):
	"""
	Create the Icarus Verilog command to launch the simulation
	"""
	cmd = "iverilog "

	if args.dotfile:
		dotfiles = " ".join(args.dotfile)
		cmd += "-f " + dotfiles + " "

	if args.include:
		incs = " ".join(args.include)
		cmd += "-I " + incs + " "

	if args.test[0][-2:] == ".v":
		testname = args.test[0][:-2] + ".vvp"
	elif args.test[0][-3:] == ".sv":
		testname = args.test[0][:-3] + ".vvp"
	else:
		print "ERROR: the test doesn't seem to be a verilog/SystermVerilog file"

	cmd += args.test[0] + " -o " + testname + "; "
	cmd += "vvp " + testname
	print cmd

def create_questasim(args):
	"""
	Create the Questasim command to launch the simulation
	"""

	cmd = "vlib work; "


if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='ThotIP Unit test runner v1.0')

	parser.add_argument('--test', dest='test', type=str, default="all", nargs="*",
						help='Unit test to run. Can be a file or a list of files')

	parser.add_argument('-f', dest='dotfile', type=str, default=None, nargs="*",
						help="A dot file (file.f) to load with incdir, define and fileset")

	parser.add_argument('--sim', dest='simulator', type=str,
						default="icarus",
						help='The simulator to use. Can be Icarus Verilog, Verilator or Questasim')

	parser.add_argument('-I', dest='include', type=str, nargs="*",
						default="", help='An include folder')

	args = parser.parse_args()

	## Lower the simulator name to ease process
	args.simulator = args.simulator.lower()
	
	if "iverilog" in args.simulator or "icarus" in args.simulator:
		create_iverilog(args)

	elif "modelsim" in args.simulator or "questa" in args.simulator:
		create_questasim(args)

