#!/usr/bin/env python3

__version__ = "0.1.0"

import os
import sys
import time
import logging
import string
import logging.config
import argparse
import datetime
import pathlib
import log2csv as lc

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


def split_daemon(daemon):
    return daemon.split("[")


def main(args):
    logger = logging.getLogger("syslog-daemon-splitter")
    logger.setLevel(args.loglevel)

    args.report_data = {}

    seen_daemons = []
    daemon_handles = {}
    daemon_metrics = {}
    # open file handles for the wanted daemons

    syslog_fieldnames = [
        "line_number",
        "line_length",
        "extracted_date",
        "unix_timestamp",
        "real_date",
        "hostname",
        "daemon",
        "wiped_line",
    ]

    logfile = pathlib.Path(args.filename)
    args.filename_stat = os.stat(logfile)
    logger.debug(logfile.parent)
    logger.debug(args.split_log_subdir)
    logger.debug(args.filename_stat.st_size)
    daemon_dir = pathlib.Path(f"""{logfile.parent}/{args.split_log_subdir}-{logfile.name}""")
    daemon_dir.parent.mkdir(parents=True, exist_ok=True)
    if not os.path.exists(daemon_dir):
        os.mkdir(daemon_dir)
    logger.debug(daemon_dir)

    args.filename_path = pathlib.Path(args.filename)
    logger.info(
        f"""Splitting logfile: {logfile} of size: {args.filename_stat.st_size}"""
    )

    # A syslog line looks like this :
    # Aug 15 08:22:53 debian systemd-modules-load[272]: Inserted module 'ppdev'
    # 0123456789ABCDEF
    # we want to extract the date so we split at 15:
    split_at_column = 15

    args.report_data["start_timestamp"] = time.time()

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
            length_of_line = len(line)
            if length_of_line <= split_at_column:
                logger.warning(
                    f"squib: line {line_number} is not minimum length of ({split_at_column}) characters"
                )
                continue
            line = line.rstrip()
            line_dict = {}
            date, remains_of_line = line[:split_at_column], line[split_at_column:]
            r = remains_of_line
            w = r.lstrip(" ")
            z = w.split(" ", 2)
            if len(z) >= 2:
                hostname = z[0]
                d = split_daemon(z[1])
                daemon = d[0]
                # This isn't me complaining. It's a warning about accepting
                # data that could come from anywhere and cleaning it up before
                # you do anything with it. There really is a daemon called `/cinnamon-killer-daemon`
                # now that sound exciting and spicy but this script it just a bit of fun
                # it won't work very well if it tries to write to `/cinnamon-killer-daemon.log`
                # and even it it did that would probably be terrible because let's face it
                # people are probably running this script as root so we'll just strip out all the
                # non alphanumberic characters from `daemon` with this:
                daemon = lc.slugify(daemon)
                # Pop a new line back on the "line":
                line = f"""{line}\n"""
                # Create a new file for each daemon if the daemon has not been seen before:
                if daemon not in seen_daemons:
                    daemon_log = f"""{daemon}.log"""
                    daemon_log = daemon_dir / daemon_log
                    daemon_handles[daemon] = open(daemon_log, "w")
                    logger.debug(
                        f"""daemon {daemon} has not been seen before opening file handle and filename is {daemon_log}"""
                    )
                    daemon_handles[daemon].write(line)
                    seen_daemons.append(daemon)
                    daemon_metrics[daemon] = {"bytes_written": 0}
                    daemon_metrics[daemon]["bytes_written"] += len(line)
                else:
                    logger.debug(
                        f"""daemon {daemon} has been seen before writing to its file"""
                    )
                    daemon_handles[daemon].write(line)
                    daemon_metrics[daemon]["bytes_written"] += len(line)
            else:
                logger.warning(
                    f"squib: line {line_number} does not have host/daemon portion."
                )
                continue

    args.report_data["input_file"] = args.filename
    args.report_data["input_file_size"] = args.filename_stat.st_size
    args.report_data["end_timestamp"] = time.time()
    args.report_data["duration"] = (
        args.report_data["end_timestamp"] - args.report_data["start_timestamp"]
    )
    args.report_data["seen_daemons"] = seen_daemons
    args.report_data["daemon_metrics"] = daemon_metrics
    args.report_data["seen_daemons_string"] = "\n  ".join(seen_daemons)
    args.report_data["seen_daemons_count"] = len(seen_daemons)

    logger.info(
        f"""\nstart: {args.report_data['start_timestamp']}\nend:{args.report_data['end_timestamp']}\nduration: {args.report_data['duration']}\ndaemons extracted ({args.report_data['seen_daemons_count']}):\n  {args.report_data['seen_daemons_string']}\n\ndaemon_metrics:\n {args.report_data['daemon_metrics']}"""
    )

    if args.sankey == True:
        print(f"""\n\n{args.filename} [{args.filename_stat.st_size}] BytesWritten\n""")
        #for daemon in daemon_metrics:
        sorted_daemon_metrics = dict(reversed(sorted(daemon_metrics.items(), key=lambda item: item[1]['bytes_written'])))
        counter = 0
        for daemon in sorted_daemon_metrics:
            print(
                f"""BytesWritten [{daemon_metrics[daemon]['bytes_written']}] {daemon}"""
            )
            if counter == 30:
                print(f"""""")
            counter +=1


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
        help="debug(-d, --debug, etc)",
    )

    parser.add_argument(
        "--base-year",
        action="store",
        dest="base_year",
        default=datetime.datetime.now().year,
        help="--base-year 2021",
    )

    parser.add_argument(
        "--csv-file",
        action="store",
        dest="csv_file",
        default="syslog.csv",
        help="--csv-file  <csv output file name>",
    )

    parser.add_argument(
        "--sankey",
        action="store_true",
        dest="sankey",
        help="Generate output for https://sankeymatic.com/build/",
    )

    parser.add_argument(
        "--log-type",
        action="store",
        dest="log_type",
        default="syslog",
        help="--log-type syslog ",
    )

    parser.add_argument(
        "--split-log-subdir",
        action="store",
        dest="split_log_subdir",
        default="split-logs",
        help="--split-log-subdir split-logs",
    )

    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__),
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
