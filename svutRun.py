#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" ThotIP Unit Test runner v1.0

Usage:
  svutRun.py [<name>...] [-sim <simulator>] [--verbose]
  svutRun.py clean [--verbose]
  svutRun.py (-h | --help)
  svutRun.py --version

Options:
  name          The unit test file name, or a list of files
  clean         Clean the current folder
  --verbose     Print info for debug purpose
  -h --help     Show this screen.
  --version     Show version.

"""

from docopt import docopt

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

if __name__ == '__main__':

    arguments = docopt(__doc__, version='ThotIP Unit Test runner v1.0')

    if arguments["--verbose"]:
        print(arguments)


