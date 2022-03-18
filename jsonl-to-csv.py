#!/usr/bin/env python3
"""
Converts an `exceptions.log` file using to CSV.
"""

__author__ = "David Morris"
__version__ = "0.1.0"
__license__ = "MIT"

import sys
import csv
import json
import logging
import argparse
import logging.config
import pathlib
import log2csv
from pathlib import Path


logging.basicConfig(stream=sys.stdout, level=logging.INFO)


def main(args):
    # create logger
    logger = logging.getLogger('root')
    FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
    logging.basicConfig(format=FORMAT)
    logger.setLevel(logging.INFO)
    #logger.setLevel(logging.DEBUG)

    p = pathlib.Path(sys.argv[1])

    status_codes = log2csv.get_wanted_kv_headers(logtype=args.log_type)
    fieldnames = status_codes[args.log_type][args.section]

    if args.csv_file is None:
        args.csv_file = f"""{args.log_type}.csv"""
        args.csv_path = pathlib.Path(args.csv_file)
    else:
        args.csv_path = pathlib.Path(args.csv_file)

    with open(args.csv_path, "w") as csvfile:
        writer = csv.DictWriter(csvfile, delimiter=",", fieldnames=fieldnames)
        if args.no_header == False:
            writer.writeheader()
        with open(p,'r') as jsonl_file:
            line_count = 0
            for line in jsonl_file:
                line_count += 1
                logger.debug(f"""line: {line_count} """)
                try:
                    json_line = json.loads(line)
                    parsed_line = {
                                k: json_line[k]
                                for k in fieldnames
                                if k in json_line
                            }
                    logger.debug(f"""{parsed_line}""")
                    writer.writerow(parsed_line)
                except:
                    next


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="a syslog file")
    parser.add_argument(
        "--log-type",
        action="store",
        dest="log_type",
        default="exceptions",
        help="--log-type the type of a the file in the log-formats.json file.",
    )
    parser.add_argument(
        "--csv-file",
        action="store",
        dest="csv_file",
        default=None,
        help="--csv-file  <csv output file name>",
    )
    parser.add_argument(
        "-n",
        "--no-header",
        action="store_true",
        help="--no-header <dont print the header in the csv",
    )
    parser.add_argument(
        "--section",
        action="store",
        dest="section",
        default="core",
        help="--section in `log-formats.json` to match against default is `core`.",
    )
    args = parser.parse_args()
    main(args)
