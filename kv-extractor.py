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
import configparser

from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class Report:
    def __init__(self):
        self.file_stats = {}
        self.ghes_config = None
        self.ghes_version = None
        self.lines_total = 0
        self.lines_parsed = 0
        self.lines_with_read_failed = 0
        self.lines_with_parse_failed = 0

    def get_ghes_config(self, gh_conf_file):
        config = configparser.ConfigParser()
        config.read(gh_conf_file)
        self.ghes_config = config

    def get_ghes_version(self):
        self.ghes_version = self.ghes_config.get('core', 'package-version')

    def __str__(self):
            return f'Report(file_stats={self.file_stats}, ghes_version={self.ghes_version})'
            #return f'Report(ghes_version={self.ghes_version}, lines_total={self.lines_total}, lines_parsed={self.lines_parsed}, lines_with_read_failed={self.lines_with_read_failed}, lines_with_parse_failed={self.lines_with_parse_failed})'


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
    report.get_ghes_config("../metadata/github.conf")
    report.get_ghes_version()
    print(report.ghes_version)

    results = {}

    for  (line_number, line, exception) in read_file_line_by_line(args.kv_input_file):
        if line is None:
            report.file_stats.setdefault(args.kv_input_file, {"lines_with_read_failed": 0, "lines_total": 0, "lines_parsed": 0, "lines_with_parse_failures": 0})["lines_with_read_failed"] += 1
            continue    
        report.file_stats.setdefault(args.kv_input_file, {"lines_with_read_failed": 0, "lines_total": 0, "lines_parsed": 0, "lines_with_parse_failures": 0})["lines_total"] += 1
        try:
           r = parse_kv(line)
           report.file_stats[args.kv_input_file]["lines_parsed"] += 1
           results.update(r)
        except Exception as e:
            report.file_stats[args.kv_input_file]["lines_with_parse_failures"] += 1

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
