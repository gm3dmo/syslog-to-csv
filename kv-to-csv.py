#!/usr/bin/env python

__version__ = "0.1.0"

import os
import sys
import csv
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

    filename = pathlib.Path(args.filename)

    logger.info(f"""filename: {args.filename}""")
    logger.info(f"""filename.stem: {filename.stem}""")

    logfile_type = filename.stem.split(".")[0]

    wanted = "core"

    status_codes = log2csv.get_wanted_kv_headers(logtype=logfile_type)
    logger.debug(f"""status_codes: {status_codes}""")

    fieldnames = status_codes[logfile_type][wanted]
    fieldnames.append("line_number")
    fieldnames.append("line_length")

    skipped_count = 0
    with open(args.csv_file, "w") as csvfile:
        writer = csv.DictWriter(csvfile, delimiter=",", fieldnames=fieldnames)
        if args.header == "yes":
            writer.writeheader()

        with open(filename, "rb") as file:
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

                if wanted == "core":
                    # delete the keys of parsed line we don't want
                    try:
                        raw_parsed_line = log2csv.parse_kv_pairs_two(
                            line.rstrip("\r\n")
                        )
                        parsed_line = {
                            k: raw_parsed_line[k]
                            for k in status_codes[logfile_type][wanted]
                            if k in raw_parsed_line
                        }
                        # line_count starts at zero. Add 1 to get
                        # line number in the file.
                        parsed_line["line_number"] = line_count + 1
                        parsed_line["line_length"] = length_of_line
                    except Exception:
                        logger.error(
                            f"""Could not parse line number: {line_count} data: {line}"""
                        )
                        continue
                    if parsed_line != {}:
                        logger.debug(f"""line: {line_count}""")
                        logger.debug(f"""PLK: {parsed_line.keys()}""")
                        if status_codes[logfile_type]["must"] not in parsed_line.keys():
                            skipped_count += 1
                            logger.debug(
                                f""" i skipped line: {line_count} because: {parsed_line.keys()} does not contain: {status_codes[logfile_type]['must']} """
                            )
                            continue
                        else:
                            pass
                        logger.debug(f"""PLK2: {parsed_line.keys()}""")
                        writer.writerow(parsed_line)
                    else:
                        logger.debug(f"""line failed to parse: {line_count}""")
                        logger.debug(f"""{line}""")
                        next

    csv_size_in_bytes = os.stat(csvfile.name).st_size
    human_size_of_csv = log2csv.sizer(csv_size_in_bytes)

    logger.info(
        f"""Converted file: {filename} size type: {logfile_type} to CSV file {csvfile.name} size {csv_size_in_bytes} bytes or roughly {human_size_of_csv}."""
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
        default=logging.WARNING,
        help="debug(-d, --debug, etc)",
    )

    parser.add_argument(
        "--csv-file",
        action="store",
        dest="csv_file",
        default="log.csv",
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
        help="--log-type the type of a the file in the log-formats.json file",
    )

    parser.add_argument(
        "--header",
        action="store",
        dest="header",
        default="yes",
        help="--header no <dont print the header in the csv",
    )

    args = parser.parse_args()

    main(args)
