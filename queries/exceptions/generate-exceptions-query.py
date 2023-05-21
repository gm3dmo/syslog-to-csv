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
SELECT strftime('%Y-%m-%dT%H:%M:%S', datetime(strftime('%s', created_at) / 600 * 600, 'unixepoch')) AS timeframe,
"""


    body = []
    # remove the final comman from teh final line

    key_of_class = {}

    classes = get_distinct_values(conn, args.table_name, "class")
    for cl in classes:
        t =  stripVowels(cl[0])
        new_class = replaceColons(t)
        key_of_class[new_class] = cl[0]
        line_template =  f"""sum(case when class like '{cl[0]}' then 1 else 0 end) as {new_class}"""
        body.append(line_template)

    middle = (',\n'.join(body))


    footer = """
FROM exceptions GROUP BY timeframe ORDER BY timeframe
"""

    print(f"""{header}{middle} {footer}""")
    for k in key_of_class.keys():
        print(f"""({k} = {key_of_class[k]})""")


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
        default="exceptions",
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
