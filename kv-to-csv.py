#!/usr/bin/env python3

__version__ = "0.1.0"

import os
import sys
import csv
import gzip
import time
import logging
import argparse
import logging.config
import pathlib
import bundlefun as bf

logger = logging.getLogger(__name__)

def main(args):
    """kv-to-csv - process a file containing key value pairs and outputs a csv file"""
    log_level = args.log_level.upper()
    logging.basicConfig(level=log_level)
    logger = logging.getLogger('bf')
    loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]

    for logger in loggers:
        logger.setLevel(level=log_level)

    logger.debug(f"""filename: {args.filename}""")

    args.report_data = {}
    args.filename_path = pathlib.Path(args.filename)
    args.file_size_bytes = bf.get_filesize(args.filename_path)
    args.file_size_human = bf.sizer(args.file_size_bytes)

    args.report_data["start_timestamp"] = time.time()

    if args.log_type is None:
        args.log_type = args.filename.stem.split(".")[0]

    if args.csv_file is None:
        args.csv_file = f"""{args.log_type}.csv"""
        args.csv_path = pathlib.Path(args.csv_file)
    else:
        args.csv_path = pathlib.Path(args.csv_file)

    args.report_data["filename_path"] = args.filename_path

    status_codes = bf.get_wanted_kv_headers(logtype=args.log_type)
    logger.debug(f"""status_codes: {status_codes}""")

    fieldnames = status_codes[args.log_type][args.section]

    if args.no_line_number is False:
        fieldnames.append("line_number")
    if args.no_line_length is False:
        fieldnames.append("line_length")

    skipped_count = 0

    with open(args.csv_path, "w") as csvhandle:
        writer = csv.DictWriter(csvhandle, delimiter=",", fieldnames=fieldnames)
        if args.no_header == False:
            writer.writeheader()
        open_fn = bf.open_file_handle(args.filename_path)
        with open_fn(args.filename_path, "rb") as file:
            lines_processed_counter = 0
            for line_count, line in enumerate(file.readlines()):
                length_of_line = len(line)
                lines_processed_counter += 1
                # Cheat section where new lines are removed
                # and comma replaced with underscore.
                try:
                    line = str(line.replace(b"\r", b"~"), "utf-8")
                    line = str(line.replace(",", "_"))
                except Exception:
                    logger.error(
                        f"""Could not parse line number: {line_count} data: {line}"""
                    )
                    continue

                if args.section == "core":
                    try:
                        logger.debug(f"""parsing raw line {line}""")
                        raw_parsed_line = bf.parse_kv_pairs_two(
                            line.rstrip("\r\n")
                        )
                        logger.debug("""parsing raw line done: {raw_parsed_line}""")
                        parsed_line = {
                            k: raw_parsed_line[k]
                            for k in status_codes[args.log_type][args.section]
                            if k in raw_parsed_line
                        }
                        # line_count starts at zero. Add 1 to get
                        # line number in the file.
                        if args.no_line_number is False:
                            parsed_line["line_number"] = line_count + 1
                        if args.no_line_length is False:
                            parsed_line["line_length"] = length_of_line
                    except Exception:
                        logger.error(
                            f"""Could not parse line number: {line_count} data: {line}"""
                        )
                        continue
                    if parsed_line != {}:
                        logger.debug(f"""line: {line_count}""")
                        logger.debug(f"""parsed line keys: {parsed_line.keys()}""")
                        if (
                            status_codes[args.log_type]["must"]
                            not in parsed_line.keys()
                        ):
                            skipped_count += 1
                            logger.debug(
                                f"""Skipped line: {line_count} because: {parsed_line.keys()} does not contain: {status_codes[args.log_type]['must']} """
                            )
                            continue
                        else:
                            pass
                        logger.debug(f"""parsed line keys2: {parsed_line.keys()}""")
                        writer.writerow(parsed_line)
                    else:
                        logger.debug(f"""line failed to parse: {line_count}""")
                        logger.debug(f"""{line}""")
                        next

    args.report_data["csv_file"] = args.csv_file
    args.report_data["skipped_count"] = skipped_count
    args.report_data["csv_size_in_bytes"] = os.stat(args.csv_file).st_size
    args.report_data["human_size_of_csv"] = bf.sizer(
        args.report_data["csv_size_in_bytes"]
    )

    logger.debug(
        f"""Converted file: {args.filename_path} size type: {args.log_type} to CSV file {args.report_data["csv_file"]} size {args.report_data["csv_size_in_bytes"]} bytes or roughly {args.report_data["human_size_of_csv"]}.\n\n"""
    )
    logger.debug(
        f"""Processed: {args.report_data["filename_path"]}\nLines in file={lines_processed_counter} lines.\nSkipped={args.report_data["skipped_count"]}\nCSV file: {args.report_data["csv_file"]} """
    )


if __name__ == "__main__":
    """Process the key value pairs found on a line and write them to a format like CSV."""
    parser = argparse.ArgumentParser()

    parser.add_argument("filename", help="a syslog file to be processed")
    parser.add_argument(
        "--log-level",
        action="store",
        dest="log_level",
        default="info",
        help="Set the log level",
    )

    parser.add_argument(
        "--csv-file",
        action="store",
        dest="csv_file",
        default=None,
        help="--csv-file  <csv output file name>",
    )

    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__),
    )

    parser.add_argument(
        "--log-type",
        action="store",
        dest="log_type",
        default="sample",
        help="--log-type the type of a the file in the log-formats.json file.",
    )

    parser.add_argument(
        "-nz",
        "--no-gz",
        action="store_true",
        help="--no-gz Input file is not gzipped.",
    )

    parser.add_argument(
        "-n",
        "--no-header",
        action="store_true",
        help="--no-header <dont print the header in the csv",
    )

    parser.add_argument(
        "-l",
        "--no-line-number",
        action="store_true",
        help="--no-line-number don't add the line number column to the csv.",
    )

    parser.add_argument(
        "-s",
        "--no-line-length",
        action="store_true",
        help="--no-line-length don't t add the line length column to the csv. ",
    )
    parser.add_argument(
        "--ghes-version",
        action="store",
        dest="ghes_version",
        help="version of ghes",
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
