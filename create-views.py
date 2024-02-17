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
import bundlefun

from bundlefun import (
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


def main(args):
    # create logger
    logger = logging.getLogger("root")
    FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
    logging.basicConfig(format=FORMAT)
    logger.setLevel(args.loglevel)

    sqlite_db = args.db_file
    conn = create_connection(sqlite_db)
    table = args.table_name
    try:
        list_of_columns = get_view_facets(table)
    except TypeError:
        raise TypeError(f"""view_facets have not been defined for table: {table}""")
        sys.exit(1)

    temporal_column = get_temporal_column(table)

    logger.info(f"""sqlite database: {sqlite_db}""")
    logger.info(f"""creating views for table: {table}""")
    logger.info(f"""views will be created for: {list_of_columns}""")
    logger.info(f"""SQL file name: {args.sql_file}""")


    report = []
    report_limit = 10
    header = f"""sqlite3 {sqlite_db} << EOF
.mode columns
.headers on
.width 60 0 0
.print '{table} Summary'
.print '---------------'"""
    report.append(header)

    for column_view in list_of_columns:
        drop_view_text = get_drop_view_text(table, column_view)
        drop_view(conn, drop_view_text)

        create_view_text = get_create_view_text(table, column_view)
        create_view(conn, create_view_text)

        # Query each view
        view_table = f"{table}_{column_view}"
        query = f"SELECT * FROM {table}_{column_view}"
        select_from_view(conn, query)

        report.append(
            f"""SELECT * FROM {table}_{column_view} order by percentage desc limit {report_limit};
.print ''"""
        )

    report.append(f""".print ''
.print '============================================================='
.print ''
.width 0 0 0
SELECT  min({temporal_column}) as "first_record", max({temporal_column}) as "last_record",  printf("%.2f", JULIANDAY(max({temporal_column})) - JULIANDAY(min({temporal_column}))) AS "span (days)" from {table} where {temporal_column} != '';""")


    print("\n".join(report))

    with open(args.sql_file, "w") as reportfn:
        reportfn.write("\n".join(report))
        reportfn.write("\nEOF\n")


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
