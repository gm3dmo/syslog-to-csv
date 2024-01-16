#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Your Name"
__version__ = "0.1.0"
__license__ = "MIT"

import sys
import shlex
import logging
import argparse
import json

from dataclasses import dataclass

@dataclass
class Report:
    lines_total: int = 0
    lines_processed: int = 0
    lines_with_errors: int = 0

logger = logging.getLogger(__name__)


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

    return result


def main(args):
    """ Main entry point of the app """

    log_level = args.log_level.upper()
    logging.basicConfig(level=log_level)
    logger = logging.getLogger(__name__)

    log_entry = sys.stdin.read()

    lines = log_entry.splitlines()

    report = Report()

    results = {}
    for i, line in enumerate(lines):
        report.lines_total+= 1
        try:
           r = parse_kv(log_entry)
           results.update(r)
        except Exception as e:
           logger.error(f"Failed to parse line {i}: {e}")

    logger.debug(f"""keys: {results.keys()}""")
    logger.debug(f"""length keys: {len(results.keys())}""")

    print("------")
    print(json.dumps(list(results.keys())))
    print("------")
    print(report)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--extension", action="store", dest="extension", default="c")

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
