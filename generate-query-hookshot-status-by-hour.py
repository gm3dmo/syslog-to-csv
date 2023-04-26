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
#import log2csv
import string

from log2csv import (
    create_connection,
    get_create_view_text,
    get_drop_view_text,
    create_view,
    drop_view,
    select_from_view,
    get_view_facets,
    get_view_facets,
    get_distinct_values
)

logging.basicConfig(stream=sys.stderr, level=logging.INFO)


def stripVowels(text):
    new_text = text.translate(str.maketrans(dict.fromkeys('aeiouAEIOU')))
    text = new_text.replace("::","_")
    return text


def replaceColons(text):
    return text.replace("::","_")


def prefixStatus(text):
    return text.replace(f"""status_{text}""")



def main(args):
    # create logger
    logger = logging.getLogger("root")
    FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
    logging.basicConfig(format=FORMAT)
    logger.setLevel(args.loglevel)

    sqlite_db = args.db_file
    conn = create_connection(sqlite_db)


    report = []
    report_limit = 10
    header = f""".mode csv
.headers on
.timer on
SELECT strftime('%Y-%m-%dT%H:00:00', time) as timeframe,
"""


    body = []
    # remove the final comman from teh final line


    values = get_distinct_values(conn, args.table_name, "status")
    for v in values:
        line_template =  f"""sum(case when status like '{v[0]}' then 1 else 0 end) as status_{v[0]}"""
        body.append(line_template)

    middle = (',\n'.join(body))


    footer = """
FROM hookshot GROUP BY timeframe ORDER BY timeframe
"""

    print(f"""{header}{middle} {footer}""")


if __name__ == "__main__":
    """This is executed when run from the command line"""
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--db-file",
        action="store",
        dest="db_file",
        default="logs.db",
        help="--db-file  <filename of sqlite db>",
    )

    parser.add_argument(
        "--table-name",
        action="store",
        dest="table_name",
        default="hookshot",
        help="--table-name",
    )

    parser.add_argument(
        "--sql-file",
        action="store",
        dest="sql_file",
        default="views.sql",
        help="--sql-file <filename sql to report view will be stored.",
    )

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
