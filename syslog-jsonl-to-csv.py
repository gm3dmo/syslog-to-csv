#!/usr/bin/env python3
"""
Converts a syslog file with jsonl file to CSV.

```
Sep  3 10:29:01 gm3dmo-076d179efe51f5709-ghe-test-ninja actions-api-server[7739]: {"logType": "ProductTrace", "logData": {"PreciseTimeStamp":"2022-09-03 10:29:01.5829","TraceId":"00000001-0001-0001-0000-000000000000"}}
````
"""

__author__ = "David Morris"
__version__ = "0.1.0"
__license__ = "MIT"

import sys
import csv
import json
import time
import logging
import argparse
import datetime
import logging.config
import pathlib
import log2csv as lc
from pathlib import Path


logging.basicConfig(stream=sys.stdout, level=logging.INFO)


def main(args):

    # create logger
    logger = logging.getLogger("root")
    FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
    logging.basicConfig(format=FORMAT)
    logger.setLevel(args.loglevel)
    logger.debug(f"""filename: {args.filename}""")

    args.report_data = {}
    args.filename_path = pathlib.Path(args.filename)
    args.output_filename = pathlib.Path(f"""{args.csv_file}""")
    args.file_size_bytes = lc.get_filesize(args.filename_path)
    args.file_size_human = lc.sizer(args.file_size_bytes)

    args.report_data["start_timestamp"] = time.time()

    logger.info(f"""filename: {args.filename_path}""")
    logger.info(f"""filename.stem: {args.filename_path.stem}""")
    logger.info(f"""filename.suffix: ({args.filename_path.suffix})""")
    logger.info(f"""filename.size: {args.file_size_human}""")
    logger.info(f"""filename.log_type: {args.log_type}""")

    # create logger
    logger = logging.getLogger("root")
    FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
    logging.basicConfig(format=FORMAT)
    # logger.setLevel(logging.INFO)
    # logger.setLevel(logging.DEBUG)

    p = pathlib.Path(sys.argv[1])

    status_codes = lc.get_wanted_kv_headers(logtype=args.log_type)
    fieldnames = status_codes[args.log_type][args.section]

    if args.no_line_number is False:
        fieldnames.append("line_number")
    if args.no_line_length is False:
        fieldnames.append("line_length")

    if args.csv_file is None:
        args.csv_file = f"""{args.log_type}.csv"""
        args.csv_path = pathlib.Path(args.csv_file)
    else:
        args.csv_path = pathlib.Path(args.csv_file)

    # A syslog line looks like this :
    # Aug 15 08:22:53 debian systemd-modules-load[272]: Inserted module 'ppdev'
    # 0123456789ABCDEF
    # we want to extract the date so we split at 15:
    split_at_column = 15

    with open(args.csv_path, "w") as csvfile:
        writer = csv.DictWriter(csvfile, delimiter=",", fieldnames=fieldnames)
        if args.no_header == False:
            writer.writeheader()

        open_fn = lc.open_file_handle(args.filename_path)
        with open_fn(args.filename_path, "rb") as file:
            for line_number, line in enumerate(file):
                try:
                    line = line.decode("utf-8")
                except Exception as e:
                    logger.warning(
                        f"Could not convert line number {line_number} to utf-8: ({line}) {e}"
                    )
                    continue
                logger.debug(f"""type line: {type(line)}""")
                length_of_line = len(line)
                logger.debug(f"processing: {line_number} ({line})")
                if length_of_line <= split_at_column:
                    logger.warning(
                        f"squib: line {line_number} is not minimum length of ({split_at_column}) characters"
                    )
                    continue
                line = line.rstrip()
                line_dict = {}
                date, remains_of_line = line[:split_at_column], line[split_at_column:]
                r = remains_of_line
                logger.debug(f"""type r: {type(r)}""")
                w = r.lstrip(" ")
                logger.debug(f"""type w: {type(w)}""")
                z = w.split(" ", 2)
                if len(z) >= 2:
                    hostname = z[0]
                    d = lc.split_daemon(z[1])
                    daemon = d[0]
                    try:
                        json_msg = json.loads(z[2])
                        logger.debug(
                            f"""line number: {line_number}: \n\n\n json_msg: ({json.dumps(json_msg, indent=4)})\n\n\n"""
                        )
                    except:
                        next

                else:
                    logger.warning(
                        f"squib: line {line_number} does not have host/daemon portion."
                    )
                    continue

                    logger.debug(f"Writing: {line_number} ({line})")
                    csv_writer.writerow(line_dict["line_number"])


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
        "-l",
        "--no-line-number",
        action="store_true",
        default=False,
        help="--no-line-number don't add the line number column to the csv.",
    )

    parser.add_argument(
        "-s",
        "--no-line-length",
        action="store_true",
        default=False,
        help="--no-line-length don't t add the line length column to the csv. ",
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
    parser.add_argument(
        "-d",
        "--debug",
        action="store_const",
        dest="loglevel",
        const=logging.DEBUG,
        default=logging.DEBUG,
        # default=logging.WARNING,
        help="debug(-d, --debug, etc)",
    )

    args = parser.parse_args()
    main(args)
