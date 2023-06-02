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

def write_logo():
    logo = """

    
                  Lets have some good old
    
     _                     _ _     ______           
    | |                   | | |    |  ___|          
    | |__  _   _ _ __   __| | | ___| |_ _   _ _ __  
    | '_ \| | | | '_ \ / _` | |/ _ \  _| | | | '_ \ 
    | |_) | |_| | | | | (_| | |  __/ | | |_| | | | |
    |_.__/ \__,_|_| |_|\__,_|_|\___\_|  \__,_|_| |_|
    
    
"""
    print(logo)


def main(args):
    write_logo()
    logger = logging.getLogger("b2c")
    logger.setLevel(args.loglevel)

    args.bundle_config_file = f"{args.bundle_dir}/metadata/github.conf"
    args.bundle_config = lc.get_gh_config(args.bundle_config_file)
    args.ghes_release = lc.get_ghes_version(args.bundle_config)
    args.ghes_feature_release = args.ghes_release[0:3]
    args.int_ghes_feature_release = int(args.ghes_feature_release.replace('.',''))


    logger.info(f"args.bundle_dir: {args.bundle_dir}")
    logger.info(f"args.bundle_config_file: {args.bundle_config_file}")
    logger.info(f"args.generate_syslog_csv: {args.generate_syslog_csv}")
    logger.info(f"args.turbo: {args.turbo}")
    logger.info(f"args.ghes_release: {args.ghes_release}")
    logger.info(f"args.ghes_feature_release: {args.ghes_feature_release}")
    logger.info(f"args.int_ghes_feature_release: {args.int_ghes_feature_release}")

    if args.int_ghes_feature_release >= 39:
        args.log_formats_filename ="log-formats-3.9.json"
    else:
        args.log_formats_filename ="log-formats.json"

    args.log_formats_file = f"""{args.bin_dir}/{args.log_formats_filename}"""

    logger.info(f"GHES release in bundle: {args.ghes_release}")
    logger.info(f"log formats file is: {args.log_formats_filename}")
    lf = lc.get_log_formats(args.log_formats_file)


    args.p = Path(".")
    args.log_directories = [
        "github-logs",
        "system-logs",
        "babeld-logs",
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
        "hookshot-go",
        "babeld",
        "gitrpcd",
        "spokesd",
    ]


    if args.generate_syslog_csv == True:
        logger.info("Adding syslog to csv conversion.")
        args.log_types.append("syslog")
    logger.info(f"args.log_types: {args.log_types}")
        

    args.sqlite_db_lines = [
        "rm logs.db",
        "sqlite3 logs.db << EOF",
        ".mode csv",
        ".separator ','",
    ]

    args.syslog_files = []

    args.report = {}

    # If there is a pypy3 interpreter on the path
    # lets use that for speed.
    pypy3_interpreter_exists = lc.is_pypy3()
    if pypy3_interpreter_exists:
        logger.info(f"""Switching interpreter to pypy3: {pypy3_interpreter_exists}""")
        args.python_interpreter = pypy3_interpreter_exists
    else:
        logger.info(f"""No pyp3 sticking with {args.python_interpreter}""")

    syslog_files = lc.create_list_of_syslog_files_to_split(args)


    MACHINE_RUNNING = True

    while MACHINE_RUNNING == True:
        logger.info(
            f"""=============== Phase 1:  Split system-logs/syslog files ==================\n\n"""
        )
        logger.info(f"""Split syslog files out to a file per daemon.\n""")
        logger.debug(f"""syslog_files: {syslog_files}""")
        for line in syslog_files:
            if args.turbo == True and (str(line).endswith(".1") or str(line).endswith(".gz")):  
                logger.info(f"""Skipping {line} because turbo flag (--turbo)  is engaged we do not procss .1 or .gz files""")
                next
            cmd = f"""{args.python_interpreter} {args.bin_dir}/{splitter} {line}"""
            try:
                subprocess.run([cmd], check=True, shell=True)
            except subprocess.CalledProcessError as err:
                logger.info("ERROR:", err)
        logger.info(f"""=============== Phase 1:  Complete ==================\n\n""")

        logger.info(
            f"""=============== Phase 2:  Convert to CSV ==================\n\n"""
        )
        files_to_convert = lc.create_list_of_files_to_convert_to_csv(args)
        for line in files_to_convert:
            cmd = line
            try:
                subprocess.run([cmd], check=True, shell=True)
            except subprocess.CalledProcessError as err:
                logger.info("ERROR:", err)

        args.report["files_to_convert"] = files_to_convert

        file_list = "\n".join(args.report["files_to_convert"])
        logger.info(f"""\n""")
        logger.info(f"""Files converted: \n\n{file_list}\n\n""")
        logger.info(f"""=============== Phase 2 Complete ==================\n\n""")
        logger.info(
            f"""=============== Phase 3: Generate sqlite database ================\n\n"""
        )
        args.sqlite_db_chunk = []
        args.sqlite_db_chunk = lc.create_list_of_csv_to_import_to_sqlite(args)
        sqlite_ddl_text = "\n".join(args.sqlite_db_chunk)

        with open(args.db_ddl_file, "w") as f:
            f.writelines(f"{sqlite_ddl_text}\n")

        # Create the database using the DDL file
        cmd = f"""logs.ddl"""
        try:
            result = subprocess.run(
                ["bash", cmd], check=True, shell=False, capture_output=True
            )
        except subprocess.CalledProcessError as err:
            logger.info("ERROR:", err)
        logger.info(f"""=============== Phase 3: Complete ================\n\n""")

        if check_db_exists(args.dbfile) == True:
            logger.info(
                f"""=============== Phase 4: Generate SQL Views ================\n\n"""
            )
            conn = lc.create_connection(args.dbfile)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            for table in tables:
                line = f"""{args.python_interpreter} {args.bin_dir}/create-views.py --db-file {args.dbfile} --table-name {table[0]} --sql-file {table[0]}.sql"""
                cmd = line
                try:
                    subprocess.run([cmd], check=True, shell=True)
                except subprocess.CalledProcessError as err:
                    logger.info("ERROR:", err)

            logger.info(f"""=============== Phase 4: Complete ================\n\n""")

            MACHINE_RUNNING = False


if __name__ == "__main__":
    """This is executed when run from the command line"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--log-level",
        action="store_const",
        dest="loglevel",
        const=logging.INFO,
        default=logging.INFO,
        help="debug(-d, --log-level, etc)",
    )

    parser.add_argument(
        "--dbfile",
        action="store",
        dest="dbfile",
        default="logs.db",
        help="name of the sqlite database",
    )

    parser.add_argument(
        "--db-ddlfile",
        action="store",
        dest="db_ddl_file",
        default="logs.ddl",
        help="database ddl file",
    )

    parser.add_argument(
        "--bin-dir",
        action="store",
        dest="bin_dir",
        default="syslog-to-csv",
        help="where the scripts live.",
    )

    parser.add_argument(
        "--bundle-dir",
        action="store",
        dest="bundle_dir",
        default=".",
        help="where the bundle lives"
    )

    parser.add_argument(
        "--generate-syslog-csv",
        action="store_true",
        help="Generate the syslog csv files",
    )

    parser.add_argument(
        "--no-generate-syslog-csv",
        action="store_false",
        dest="generate-syslog-csv",
        help="Dont generating the syslog csv files",
    )

    parser.add_argument(
        "--turbo",
        action="store_true",
        help="Skip the .1 files.",
    )

    parser.add_argument(
        "--no-turbo",
        action="store_false",
        dest="turbo_mode",
        help="Generate from .1 log files.",
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
