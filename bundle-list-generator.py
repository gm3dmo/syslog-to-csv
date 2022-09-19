#!/usr/bin/env python3

__version__ = "0.1.0"

import sqlite3
import sys
import json
import logging
import logging.config
import argparse
import datetime
import pathlib
from pathlib import Path
import log2csv as lc
from pathlib import Path

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


def main(args):
    logger = logging.getLogger("bundle-list-generator")
    logger.setLevel(args.loglevel)
    args.p = Path(".")
    args.bin_dir = "syslog-to-csv"
    args.log_directories = [
        "github-logs",
        "system-logs",
        "system-logs/split-logs-syslog",
        "system-logs/split-logs-syslog.1",
    ]

    args.log_types = [
        "unicorn",
        "exceptions",
        "auth",
        "gitauth",
        "syslog",
        "hookshot-go",
        "babeld",
        "gitrpcd",
        "spokesd",
    ]

    args.files_to_convert = lc.create_list_of_files_to_convert(args)
    logger.debug(args.files_to_convert)

    args.log_list = lc.create_list_of_files_to_convert(args)

    for file in args.log_list:
        logger.info(file)


if __name__ == "__main__":
    """This is executed when run from the command line"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d",
        "--debug",
        action="store_const",
        dest="loglevel",
        const=logging.DEBUG,
        default=logging.WARNING,
        help="debug(-d, --debug, etc)",
    )
    parser.add_argument(
        "--python-interpreter",
        action="store",
        dest="python_interpreter",
        default="pypy3",
        help="defines the python interpreter used: --python-interpreter /usr/bin/python",
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__),
    )
    args = parser.parse_args()

    main(args)
