#!/usr/bin/env python

__version__ = "0.1.0"

import os
import sys
import csv
import gzip
import logging
import argparse
import logging.config
import pathlib
import log2csv

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


@log2csv.timeit
def main(args):
    # create logger
    logger = logging.getLogger("root")
    FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
    logging.basicConfig(format=FORMAT)
    logger.setLevel(args.loglevel)

    logger.debug(f"""filename: {args.filename}""")

    args.filename_path = pathlib.Path(args.filename)
    args.file_size_bytes = log2csv.get_filesize(args.filename_path)
    args.file_size_human = log2csv.sizer(args.file_size_bytes)

    if args.log_type is None:
        args.log_type = args.filename.stem.split(".")[0]

    if args.csv_file is None:
        args.csv_file = f"""{args.log_type}.csv"""
        args.csv_path = pathlib.Path(args.csv_file)
    else:
        args.csv_path = pathlib.Path(args.csv_file)

    logger.info(f"""filename: {args.filename_path}""")
    logger.info(f"""filename.stem: {args.filename_path.stem}""")
    logger.info(f"""filename.suffix: {args.filename_path.suffix}""")
    logger.info(f"""filename.size: {args.file_size_human}""")
    logger.info(f"""filename.log_type: {args.log_type}""")

    status_codes = log2csv.get_wanted_kv_headers(logtype=args.log_type)
    logger.debug(f"""status_codes: {status_codes}""")

    fieldnames = status_codes[args.log_type][args.section]

    if args.no_line_number is False:
        fieldnames.append("line_number")
    if args.no_line_length is False:
        fieldnames.append("line_length")

    skipped_count = 0


    with open(args.csv_path, "w") as csvfile:
        writer = csv.DictWriter(csvfile, delimiter=",", fieldnames=fieldnames)
        if args.no_header == False:
            writer.writeheader()
        open_fn = gzip.open if log2csv.is_gzipped(args.filename_path) else open
        with open_fn(args.filename_path, "rb") as file:
            line_count = 0
            for line_count, line in enumerate(file.readlines()):
                length_of_line = len(line)
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
                    # delete the keys of parsed line we don't want
                    try:
                        raw_parsed_line = log2csv.parse_kv_pairs_two(
                            line.rstrip("\r\n")
                        )
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

    csv_size_in_bytes = os.stat(csvfile.name).st_size
    human_size_of_csv = log2csv.sizer(csv_size_in_bytes)

    logger.info(
        f"""Converted file: {args.filename} size type: {args.log_type} to CSV file {csvfile.name} size {csv_size_in_bytes} bytes or roughly {human_size_of_csv}."""
    )
    logger.info(f"""Skipped={skipped_count} Lines in file={line_count} lines.""")


if __name__ == "__main__":
    """This is executed when run from the command line"""
    parser = argparse.ArgumentParser()

    parser.add_argument("filename", help="a syslog file")

    parser.add_argument(
        "-d",
        "--debug",
        action="store_const",
        dest="loglevel",
        const=logging.DEBUG,
        default=logging.INFO,
        #default=logging.WARNING,
        help="debug(-d, --debug, etc)",
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
        "--section",
        action="store",
        dest="section",
        default="core",
        help="--section in `log-formats.json` to match against default is `core`.",
    )

    args = parser.parse_args()

    main(args)