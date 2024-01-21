#!/usr/bin/env python3
"""
An experiment in extracting key value pairs from files.
"""

__author__ = "David Morris gm3dmo@gmail.com"
__version__ = "0.1.0"

import json
import logging
import argparse
import bundlefun as bf

logger = logging.getLogger(__name__)


def main(args):
    log_level = args.log_level.upper()
    logging.basicConfig(level=log_level)
    logger = logging.getLogger(__name__)

    report = bf.Report()
    #report.get_ghes_config("../metadata/github.conf")
    print(report.ghes_feature_version)

    results = {}

    for  (line_number, line, exception) in bf.read_file_line_by_line(args.kv_input_file):
        if line is None:
            report.file_stats.setdefault(args.kv_input_file, {"lines_with_read_failed": 0, "lines_total": 0, "lines_parsed": 0, "lines_with_parse_failures": 0})["lines_with_read_failed"] += 1
            continue    
        report.file_stats.setdefault(args.kv_input_file, {"lines_with_read_failed": 0, "lines_total": 0, "lines_parsed": 0, "lines_with_parse_failures": 0})["lines_total"] += 1
        try:
           r = bf.parse_kv(line)
           report.file_stats[args.kv_input_file]["lines_parsed"] += 1
           results.update(r)
        except Exception as e:
            report.file_stats[args.kv_input_file]["lines_with_parse_failures"] += 1

    logger.debug(f"""keys: {results.keys()}""")

    report.file_stats[args.kv_input_file]["kv_pairs_extracted"] = len(results.keys())
    
    keys_extracted = len(results.keys())

    print("------")
    print(json.dumps(list(results.keys())))
    print("------")

    print(report)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('kv_input_file', help='Full path to a log file to process')
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
