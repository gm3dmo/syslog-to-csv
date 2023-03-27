#!/usr/bin/env python3

__version__ = "0.1.0"

import sqlite3
import os
import sys
import json
import time
import logging
import logging.config
import argparse
import datetime
import pathlib
import subprocess
from pathlib import Path
import log2csv as lc
from pathlib import Path

logging.basicConfig(stream=sys.stderr, level=logging.INFO)


def check_db_exists(dbfile):
    status = False
    if os.path.isfile(dbfile):
        if lc.create_connection(dbfile):
            status = True
    return status


def main(args):
    logger = logging.getLogger("bundle-list-generator")
    logger.setLevel(args.loglevel)
    args.p = Path(".")
    args.bin_dir = "syslog-to-csv"
    args.log_directories = [
        "github-logs",
        "system-logs",
        "system-logs/split-logs-syslog",
        "system-logs/split-logs-syslog.1",
    ]

    priority_logs = []
    splitter = "syslog-daemon-splitter.py"

    args.log_types = [
        "unicorn",
        "exceptions",
        "auth",
        "gitauth",
        "syslog",
        "hookshot-go",
        "babeld",
        "gitrpcd",
        "spokesd",
    ]

    args.sqlite_db_lines = [
        "rm logs.db",
        "sqlite3 logs.db << EOF",
        ".mode csv",
        ".separator ','",
    ]

    args.syslog_files = []

    # bin_dir = "syslog-to-csv"
    args.bin_dir = "."

    (
        files_to_convert,
        sqlite_db_chunk,
        syslog_files,
    ) = lc.create_list_of_files_to_convert(args)

    MACHINE_RUNNING = True
    BOBBY_INTEGER = 0

    while MACHINE_RUNNING == True:
        logger.info(f"""Phase 1: Split syslog files out to a file per daemon""")
        for line in syslog_files:
            cmd = f"""{args.python_interpreter} {splitter} {line}"""
            try:
                subprocess.run([cmd], check=True, shell=True)
            except subprocess.CalledProcessError as err:
                logger.info("ERROR:", err)

        print(f"""Converting {len(files_to_convert)} files.""")
        print(f"""Converting: {files_to_convert}""")
        (
            files_to_convert,
            sqlite_db_chunk,
            syslog_files,
        ) = lc.create_list_of_files_to_convert(args)
        logger.info(f"""XXX SQLITE DDL: {len(sqlite_db_chunk)}""")

        logger.info(f"""Phase 2a: Generate Sankey Information based on file size""")
        logger.info(f"""Converting: {len(files_to_convert)}""")

        logger.info(f"""Converting: {files_to_convert}""")
        logger.info(f"""Phase 2b: Convert log files to CSV""")
        print(f"""\n""")

        for line in files_to_convert:
            cmd = line
            try:
                subprocess.run([cmd], check=True, shell=True)
            except subprocess.CalledProcessError as err:
                logger.info("ERROR:", err)

        logger.info(f"""Phase 3: Generate sqlite database from csv files""")
        logger.info(f"""SQLITE DDL: {len(sqlite_db_chunk)}""")


        sqlite_db_chunk = []
        logger.info(f"""XXXx SQLITE DDL: {len(sqlite_db_chunk)}""")
        (
            files_to_convert,
            sqlite_db_chunk,
            syslog_files,
        ) = lc.create_list_of_files_to_convert(args)

        logger.info(f"""XXXx SQLITE DDL: {len(sqlite_db_chunk)}""")

        sqlite_ddl_text = '\n'.join(sqlite_db_chunk)
        logger.info(f"""--------_---------""")
        logger.info(f"""SQLITE DDL: {sqlite_ddl_text}""")
        logger.info(f"""--------_---------""")

        with open(args.db_ddl_file, "w") as f:
            f.writelines(f"{sqlite_ddl_text}\n")
                

        sys.exit()
        time.sleep(5)


        if check_db_exists(args.dbfile) == True:
            MACHINE_RUNNING = False


if __name__ == "__main__":
    """This is executed when run from the command line"""
    parser = argparse.ArgumentParser()
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
        "--dbfile",
        action="store",
        dest="dbfile",
        default="logs.db",
        help="name of the sqlite database",
    )

    parser.add_argument(
        "---db-ddlfile",
        action="store",
        dest="db_ddl_file",
        default="logs.ddl",
        help="database",
    )

    parser.add_argument(
        "--python-interpreter",
        action="store",
        dest="python_interpreter",
        default="python3",
        help="defines the python interpreter used: --python-interpreter /usr/bin/python",
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__),
    )
    args = parser.parse_args()

    main(args)
