#!/usr/bin/env python3

__version__ = "0.1.0"

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
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

log_types = ['unicorn', 'exceptions', 'auth', 'gitauth', 'production', 'syslog' ]

def get_processor(log_type):
    p = pathlib.Path(__file__)
    log_formats_file = p.parent / "log-formats.json"
    kv_headers = {}
    with open(log_formats_file) as json_file:
        data = json.load(json_file)
        if log_type in data:
            kv_headers[logtype] = {}
            return data[logtype]["processor"]

    if  log_type == 'syslog':
        return 'syslog-to-csv.py'
    if  log_type == 'exceptions':
        return 'jsonl-to-csv.py'
    else:
        return 'kv-to-csv.py'

def main(args):
    p = Path('.')
    bin_dir = 'syslog-to-csv'
    log_directories =[ 'github-logs', 'system-logs' ]
    python_interpreter = 'pypy3'
    for log_directory in log_directories:
       for log_type in log_types:
           glob_string = f"""{log_directory}/{log_type}*"""
           # lookup the processor for log_type
           processor = get_processor(log_type)
           for item in list(p.glob(glob_string)):
              csv_file = f"""{item}.csv"""
              print(f"""pypy3 {bin_dir}/{processor} {item} --log-type {log_type} --csv-file {csv_file}""")

if __name__ == "__main__":
    """ This is executed when run from the command line """
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
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__),
    )
    args = parser.parse_args()

    main(args)