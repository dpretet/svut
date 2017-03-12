#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" ThotIP Unit Test runner v1.0

Usage:
  svutRun.py [<name>...] [--verbose]
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

if __name__ == '__main__':

    """

    """

    arguments = docopt(__doc__, version='ThotIP Unit Test runner v1.0')

    if arguments["--verbose"]:
        print(arguments)


