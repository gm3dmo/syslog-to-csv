#!/usr/bin/env python

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
import log2csv

from log2csv import create_connection, get_create_view_text, get_drop_view_text, create_view, drop_view, select_from_view

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


@log2csv.timeit
def main(args):
    # create logger
    logger = logging.getLogger("root")
    FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
    logging.basicConfig(format=FORMAT)
    logger.setLevel(args.loglevel)

    sqlite_db = '../logs.db'
    conn = create_connection(sqlite_db)
    table = "auth"
    list_of_columns = ['ip',
            'login', 'user_id', 'raw_login', 'user_agent',
            'repo', 'url', 'failure_type', 'failure_reason',
            'method', 'from', 'hashed_token', 'message'
            'protocol',
            ]

    for column_view in list_of_columns:
        drop_view_text = get_drop_view_text(table, column_view)
        drop_view(conn, drop_view_text)

        create_view_text = get_create_view_text(table, column_view)
        create_view(conn, create_view_text)
        
        # Query each view
        view_table = f"{table}_{column_view}" 
        query = f"SELECT * FROM {table}_{column_view}"
        select_from_view(conn, query)

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
        # default=logging.WARNING,
        help="debug(-d, --debug, etc)",
    )

    args = parser.parse_args()
    main(args)