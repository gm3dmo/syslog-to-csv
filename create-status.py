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

from log2csv import (
    create_connection,
    get_create_view_text,
    get_drop_view_text,
    create_view,
    drop_view,
    select_from_view,
    get_view_facets,
    get_temporal_column,
)

logging.basicConfig(stream=sys.stderr, level=logging.INFO)


def get_sql_status_query(table, divisor, temporal_column):
    query = f"""SELECT strftime('%Y-%m-%d %H:%M:%S', datetime(strftime('%s', now) / {divisor} * {divisor}, 'unixepoch')) AS bucket,
SUM(CASE WHEN status like '20%' THEN 1 ELSE 0 END) AS status_20x,
SUM(CASE WHEN status = '401' THEN 1 ELSE 0 END) AS status_401,
SUM(CASE WHEN status = '403' THEN 1 ELSE 0 END) AS status_403,
SUM(CASE WHEN status = '404' THEN 1 ELSE 0 END) AS status_404,
SUM(CASE WHEN status = '50%' THEN 1 ELSE 0 END) AS status_50x
from {table}
GROUP BY bucket, status
ORDER BY bucket ASC;"""
    return query


def main(args):
    # create logger
    logger = logging.getLogger("root")
    FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
    logging.basicConfig(format=FORMAT)
    logger.setLevel(args.loglevel)

    sqlite_db = args.db_file
    conn = create_connection(sqlite_db)
    table = args.table_name

    temporal_column = get_temporal_column(table)

    logger.info(f"""sqlite database: {sqlite_db}""")
    logger.info(f"""creating 60,30,15,5 minute queries for table: {table} using {temporal_column}""")

    report = []
    divisors = [ 300, 600, 1200, 3600 ]
    
    for divisor in divisors:
         report_file_name = f"""{table}_status_{divisor}"""
         logger.info(f"""{report_file_name}""")
         query = get_sql_status_query(table, divisor, temporal_column)

         print(f"""{query}""")
         print()

    header = f"""sqlite3 {sqlite_db} << EOF
.mode columns
.headers on
.width 60 0 0
.print '{table} Time Summary'
.print '---------------------'"""
    report.append(header)





    report.append(f""".print ''
.print '============================================================='
""")

    print("\n".join(report))

    with open(args.sql_file, "w") as reportfn:
        reportfn.write("\n".join(report))
        reportfn.write("\nEOF\n")


if __name__ == "__main__":
    """Creates a sql report for time periods for a given table."""
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
        default="auth",
        help="--table-name  <name of table for which to create views/facets>",
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
