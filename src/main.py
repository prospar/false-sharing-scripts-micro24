#!/usr/bin/env python
import sys

import tasks
from cmdlineparser import CmdLineParser


def main():
    # Parse the command line arguments and initialize options
    _options = CmdLineParser().parse(sys.argv)
    tasks.runAllTasks(_options)


if __name__ == "__main__":
    main()
