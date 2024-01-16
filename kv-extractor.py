#!/usr/bin/env python3
"""
An experiment in extracting key value pairs from files.
"""

__author__ = "David Morris gm3dmo@gmail.com"
__version__ = "0.1.0"

import sys
import shlex
import logging
import argparse
import json

from dataclasses import dataclass


logger = logging.getLogger(__name__)


@dataclass
class Report:
    # Report on the number of lines processed/failed etc.
    lines_total: int = 0
    lines_parsed: int = 0
    lines_with_read_failed: int = 0
    lines_with_parse_failed: int = 0


def parse_kv(text):
    tokenizer = shlex.shlex(text, posix=True)
    tokenizer.commenters = ""
    tokenizer.whitespace_split = True
    tokenizer.whitespace = " "
    result = {}

    for token in tokenizer:
        if "=" in token:
            logging.debug(f"""token: {token}""")
            key, value = token.split("=", 1)  # Split at the first equal sign only
            result[key] = value
        else:
            logging.debug(f"""token: {token} has no = sign to split on""")

    return result


def read_file_line_by_line(filename):
    try:
        with open(filename, 'r') as file:
            for line_number, line in enumerate(file, start=1):
                yield line_number, line, None
    except Exception as e:
        yield line_number, None, str(e)


def main(args):
    log_level = args.log_level.upper()
    logging.basicConfig(level=log_level)
    logger = logging.getLogger(__name__)

    report = Report()
    results = {}

    for  (line_number, line, exception) in read_file_line_by_line(args.kv_input_file):
        if line is None:
            logger.warning(f"failed to read {args.kv_input_file} at line:{line_number}")
            report.lines_with_read_failed += 1
            continue    
        report.lines_total+= 1
        try:
           r = parse_kv(line)
           report.lines_parsed += 1
           results.update(r)
        except Exception as e:
            logger.warning(f"failed to parse the file {args.kv_input_file} at line:{line_number}: {e}")
            report.lines_with_parse_failures += 1

    logger.debug(f"""keys: {results.keys()}""")
    logger.debug(f"""length keys: {len(results.keys())}""")

    print("------")
    print(json.dumps(list(results.keys())))
    print("------")
    print(report)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('kv_input_file', help='Path to the log file the script should process.')
    parser.add_argument(
        "-l",
        "--log-level",
        action="store",
        dest="log_level",
        default="info",
        help="Set the log level",
    )

    args = parser.parse_args()

    main(args)
