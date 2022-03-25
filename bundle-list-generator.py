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

log_types = ['unicorn', 'exceptions', 'auth', 'gitauth', 'production', 'syslog' ]
skip_list = ['system-logs/auth']

def get_processor(log_type):
    p = pathlib.Path(__file__)
    log_formats_file = p.parent / "log-formats.json"
    kv_headers = {}
    with open(log_formats_file) as json_file:
        data = json.load(json_file)
        if log_type in data:
            kv_headers[log_type] = {}
            return data[log_type]["processor"]

    if  log_type == 'syslog':
        return 'syslog-to-csv.py'
    if  log_type == 'exceptions':
        return 'jsonl-to-csv.py'
    else:
        return 'kv-to-csv.py'

def main(args):
    logger = logging.getLogger("syslog-to-csv")
    logger.setLevel(args.loglevel)

    p = Path('.')
    bin_dir = 'syslog-to-csv'
    log_directories =[ 'github-logs', 'system-logs' ]
    for log_directory in log_directories:
       for log_type in log_types:
           glob_string = f"""{log_directory}/{log_type}*"""
           for skip_listed_log in skip_list:
               logger.debug(f"""Processing skip list: {skip_listed_log}""")
               if glob_string.startswith(skip_listed_log):
                   logger.debug(f"""skip_list match: {skip_listed_log} == {glob_string}""")
                   next
               else:
                   logger.debug(f"""not a match: {skip_listed_log} == {glob_string}""")
                   # lookup the processor for log_type
                   processor = get_processor(log_type)
                   for item in list(p.glob(glob_string)):
                      if item.endswith('.csv'):
                          next
                      else:
                         csv_file = f"""{item}.csv"""
                         print(f"""{args.python_interpreter} {bin_dir}/{processor} {item} --log-type {log_type} --csv-file {csv_file}""")

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