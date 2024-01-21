#!/usr/bin/env python3
"""
An experiment in extracting key value pairs from files.
"""

__author__ = "David Morris gm3dmo@gmail.com"
__version__ = "0.1.0"

import re
import sys
import csv
import json
import gzip
import time
import shlex
import shutil
import pathlib
import sqlite3
import logging
import argparse
import datetime
import unicodedata
import configparser
import logging.config

from dataclasses import dataclass


logger = logging.getLogger(__name__)

@dataclass
class Report:
    def __init__(self):
        self.file_stats = {}
        self.ghes_config = None
        self.ghes_version = None
        self.ghes_feature_version = None
        self.lines_total = 0
        self.lines_parsed = 0
        self.lines_with_read_failed = 0
        self.lines_with_parse_failed = 0
        self.kv_pairs_extracted = 0

    def get_ghes_config(self, gh_conf_file):
        config = configparser.ConfigParser()
        config.read(gh_conf_file)
        self.ghes_config = config
        self.get_ghes_version()
        self.get_ghes_feature_version()

    def get_ghes_version(self):
        self.ghes_version = self.ghes_config.get('core', 'package-version')

    def get_ghes_feature_version(self):
        # https://docs.github.com/en/enterprise-server@3.11/admin/overview/about-upgrades-to-new-releases
        release, feature, patch = self.ghes_version.split('.')
        self.ghes_feature_version = (f"{release}.{feature}")

    def __str__(self):
            return f'Report(file_stats={self.file_stats}, ghes_version={self.ghes_version}, ghes_feature_version={self.ghes_feature_version}, lines_total={self.lines_total}, lines_parsed={self.lines_parsed}, lines_with_read_failed={self.lines_with_read_failed}, lines_with_parse_failed={self.lines_with_parse_failed}, kv_pairs_extracted={self.kv_pairs_extracted})'


def parse_kv(text):
    tokenizer = shlex.shlex(text, posix=True)
    tokenizer.commenters = ""
    tokenizer.whitespace_split = True
    tokenizer.whitespace = " "
    result = {}

    for token in tokenizer:
        if "=" in token:
            logging.debug(f"""token: {token}""")
            key, value = token.split("=", 1)  # Split at the first equal sign only
            result[key] = value
        else:
            logging.debug(f"""token: {token} has no = sign to split on""")

    return result


def read_file_line_by_line(filename):
    try:
        with open(filename, 'r') as file:
            for line_number, line in enumerate(file, start=1):
                yield line_number, line, None
    except Exception as e:
        yield line_number, None, str(e)



def get_gh_config(gh_conf_file="github.conf"):
    config = configparser.ConfigParser()
    config.read(conf_file)
    return config


def get_ghes_version(ghes_config):
    ghes_version = ghes_config.get('core', 'package-version')
    return ghes_version


def is_pypy3():
    return shutil.which("pypy3")


def get_distinct_values(conn, table, column):
    data = False
    try:
        c = conn.cursor()
        query = f"""select distinct({column}) from {table}"""
        data = c.execute(query)
    except Exception as e:
        logger.error(f"""{e}""")
    return data


def create_connection(sqliteDB):
    conn = None
    try:
        conn = sqlite3.connect(sqliteDB)
        return conn
    except Exception as e:
        logger.error(f"""{e}""")
    return conn


def get_create_view_text(table, column):
    return f"""create view {table}_{column} as select {table}.'{column}', count() as count_of,  round(100.0 * count() / (select count() from {table}), 2) as percentage from {table} group by {table}.'{column}';"""


def get_drop_view_text(table, column):
    return f"""drop view percentage_of_{column};"""


def create_view(conn, create_view_sql):
    try:
        c = conn.cursor()
        logger.info(f"""{create_view_sql}""")
        c.execute(create_view_sql)
    except Exception as e:
        logger.error(f"""{e}""")


def drop_view(conn, drop_view_sql):
    try:
        c = conn.cursor()
        logger.info(f"""{drop_view_sql}""")
        c.execute(drop_view_sql)
    except Exception as e:
        logger.error(f"""{e}""")


def select_from_view(conn, query):
    try:
        c = conn.cursor()
        logger.info(f"""select from view: {query}""")
        c.execute(query)
    except Exception as e:
        logger.error(f"""{e}""")


def get_log_type(path):
    log_type = path.stem.split(".")[0]
    return log_type


def create_list_of_syslog_files_to_split(args):
    log_list = []
    count_of_log_types = {}
    syslog_files = []
    sqlite_db_chunk = args.sqlite_db_lines
    logger.debug(f"""count_of_log_types: {count_of_log_types}""")

    for lt in args.log_types:
        count_of_log_types[lt] = 0

    for log_directory in args.log_directories:
        logger.debug(log_directory)
        glob_string = f"""{log_directory}/*"""
        for item in list(args.p.glob(glob_string)):
            logger.debug(f"""{item.name}""")
            if args.turbo == True and (str(item).endswith(".1") or str(item).endswith(".gz")):
                logger.info(f"""Skipping {item} because turbo engaged""")
                continue
            if str(item).endswith(".csv"):
                continue
            if str(item).endswith(".backup"):
                continue
            if item.name.startswith("syslog"):
                syslog_files.append(item)
                logger.debug(f"{item.name}")

    return syslog_files


def create_list_of_files_to_convert_to_csv(args):
    log_list = []
    count_of_log_types = {}
    sqlite_db_chunk = args.sqlite_db_lines
    logger.debug(f"""count_of_log_types: {count_of_log_types}""")

    for lt in args.log_types:
        count_of_log_types[lt] = 0

    for log_directory in args.log_directories:
        logger.debug(log_directory)
        glob_string = f"""{log_directory}/*"""
        for item in list(args.p.glob(glob_string)):
            if str(item).endswith(".csv"):
                continue
            if str(item).endswith(".backup"):
                continue
            if str(item).startswith("system-logs/auth.log"):
                continue
            else:
                log_type = get_log_type(item)
                if log_type in args.log_types:
                    table_name = get_table_name(log_type)
                    if table_name == False:
                        table_name = log_type
                    processor = get_processor(log_type)
                    csv_file = f"""{item}.csv"""
                    log_list.append(
                        f"""{args.python_interpreter} {args.bin_dir}/{processor} {item} --log-type {log_type} --csv-file {csv_file}"""
                    )
    logger.debug(f"""end count_of_log_types: {count_of_log_types}""")
    return log_list


def create_list_of_csv_to_import_to_sqlite(args):
    log_list = []
    count_of_log_types = {}
    sqlite_db_chunk = args.sqlite_db_lines
    logger.debug(f"""count_of_log_types: {count_of_log_types}""")

    for lt in args.log_types:
        count_of_log_types[lt] = 0

    for log_directory in args.log_directories:
        logger.debug(log_directory)
        glob_string = f"""{log_directory}/*"""
        for item in list(args.p.glob(glob_string)):
            logger.debug(f"""{item.name}""")
            if str(item).endswith(".csv"):
                continue
            if str(item).endswith(".backup"):
                continue
            if item.name.startswith("syslog"):
                continue
            else:
                log_type = get_log_type(item)
                if log_type in args.log_types:
                    table_name = get_table_name(log_type)
                    if table_name == False:
                        table_name = log_type
                    processor = get_processor(log_type)
                    logger.debug(item)
                    csv_file = f"""{item}.csv"""
                    log_list.append(
                        f"""{args.python_interpreter} {args.bin_dir}/{processor} {item} --log-type {log_type} --csv-file {csv_file}"""
                    )
                    if count_of_log_types[log_type] == 0:
                        sqlite_db_chunk.append(f""".import {csv_file} {table_name}""")
                        count_of_log_types[log_type] += 1
                        logger.debug(
                            f"""====> {log_type}: zero count {count_of_log_types[log_type]}"""
                        )
                    else:
                        sqlite_db_chunk.append(
                            f""".import "|tail -n +2 {csv_file}" {table_name} """
                        )
                        count_of_log_types[log_type] += 1
                        logger.debug(
                            f"""----> {log_type}: count {count_of_log_types[log_type]}"""
                        )
    logger.debug(f"""end count_of_log_types: {count_of_log_types}""")
    sqlite_db_chunk.append(f"""EOF""")
    return sqlite_db_chunk


def create_list_of_files_to_convert(args):
    log_list = []
    count_of_log_types = {}
    syslog_files = []
    logger.debug(f"""count_of_log_types: {count_of_log_types}""")

    for lt in args.log_types:
        count_of_log_types[lt] = 0

    for log_directory in args.log_directories:
        logger.debug(log_directory)
        glob_string = f"""{log_directory}/*"""
        for item in list(args.p.glob(glob_string)):
            logger.debug(f"""{item.name}""")
            if str(item).endswith(".csv"):
                continue
            if str(item).endswith(".backup"):
                continue
            if item.name.startswith("syslog"):
                syslog_files.append(item)
                logger.debug(f"{item.name}")

            else:
                log_type = get_log_type(item)
                if log_type in args.log_types:
                    table_name = get_table_name(log_type)
                    if table_name == False:
                        table_name = log_type
                    processor = get_processor(log_type)
                    logger.debug(item)
                    csv_file = f"""{item}.csv"""
                    log_list.append(
                        f"""{args.python_interpreter} {args.bin_dir}/{processor} {item} --log-type {log_type} --csv-file {csv_file}"""
                    )
                    if count_of_log_types[log_type] == 0:
                        sqlite_db_chunk.append(f""".import {csv_file} {table_name}""")
                        count_of_log_types[log_type] += 1
                        logger.debug(
                            f"""====> {log_type}: zero count {count_of_log_types[log_type]}"""
                        )
                    else:
                        sqlite_db_chunk.append(
                            f""".import "|tail -n +2 {csv_file}" {table_name} """
                        )
                        count_of_log_types[log_type] += 1
                        logger.debug(
                            f"""----> {log_type}: count {count_of_log_types[log_type]}"""
                        )
    logger.debug(f"""end count_of_log_types: {count_of_log_types}""")
    logger.info(f"COUNTER: ")
    sqlite_db_chunk.append(f"""EOF""")
    return (log_list, sqlite_db_chunk, syslog_files)


def get_table_name(log_type):
    p = pathlib.Path(__file__)
    log_formats_file = p.parent / "log-formats.json"
    kv_headers = {}
    with open(log_formats_file) as json_file:
        data = json.load(json_file)
        if log_type in data:
            kv_headers[log_type] = {}
            table_name = False
            if "table_name" in data[log_type]:
                table_name = data[log_type]["table_name"]
            return table_name


def get_temporal_column(log_type):
    p = pathlib.Path(__file__)
    log_formats_file = p.parent / "log-formats.json"
    kv_headers = {}
    if log_type == "hookshot":
        log_type = "hookshot-go"

    with open(log_formats_file) as json_file:
        data = json.load(json_file)
        if log_type in data:
            temporal = False
            if "temporal" in data[log_type]:
                temporal = data[log_type]["temporal"][0]
                return temporal 
            else:
                return False


def get_view_facets(log_type):
    p = pathlib.Path(__file__)
    log_formats_file = p.parent / "log-formats.json"
    kv_headers = {}
    if log_type == "hookshot":
        log_type = "hookshot-go"

    with open(log_formats_file) as json_file:
        data = json.load(json_file)
        if log_type in data:
            kv_headers[log_type] = {}
            table_name = False
            if "view_facets" in data[log_type]:
                view_facets = data[log_type]["view_facets"]
                return view_facets
            else:
                return False


def get_processor(log_type):
    p = pathlib.Path(__file__)
    log_formats_file = p.parent / "log-formats.json"
    kv_headers = {}
    with open(log_formats_file) as json_file:
        data = json.load(json_file)
        if log_type in data:
            kv_headers[log_type] = {}
            return data[log_type]["processor"]

    if log_type == "syslog":
        return "syslog-to-csv.py"
    if log_type == "exceptions":
        return "jsonl-to-csv.py"
    else:
        return "kv-to-csv.py"


def split_daemon(daemon):
    return daemon.split("[")


def syslog_fieldnames():
    return [
        "line_number",
        "line_length",
        "extracted_date",
        "unix_timestamp",
        "real_date",
        "hostname",
        "daemon",
        "wiped_line",
    ]


def slugify(value):
    """
    Converts to lowercase, removes non-word characters (alphanumerics and
    underscores) and converts spaces to hyphens. Also strips leading and
    trailing whitespace.
    """
    value = (
        unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    )
    value = re.sub("[^\w\s-]", "", value).strip().lower()
    return re.sub("[-\s]+", "-", value)


def is_gzipped(path):
    if path.suffix == ".gz":
        return True


def open_file_handle(fn):
    open_fh = gzip.open if is_gzipped(fn) else open
    return open_fh


def get_wanted_kv_headers(logtype="sample", extract_type="core"):
    p = pathlib.Path(__file__)
    log_formats_file = p.parent / "log-formats.json"
    logging.info(f"""log_formats_file used: {log_formats_file}""")
    kv_headers = {}
    with open(log_formats_file) as json_file:
        data = json.load(json_file)
        if logtype in data:
            logging.info(
                f"""logtype ({logtype}) is known and can be processed: {logtype}
extracting {len(data[logtype]['core'])} kv fields"""
            )
            kv_headers[logtype] = {}
            kv_headers[logtype]["core"] = data[logtype]["core"]
            kv_headers[logtype]["must"] = data[logtype]["must"]
        else:
            logging.error(f""": filetype is not known: {logtype}""")
    return kv_headers


def sizer(size):
    for x in ["bytes", "KB", "MB", "GB", "TB"]:
        if size < 1024.0:
            return "%3.1f %s" % (size, x)
        size /= 1024.0
    return size


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if "log_time" in kw:
            name = kw.get("log_name", method.__name__.upper())
            kw["log_time"][name] = int((te - ts) * 1000)
        else:
            duration = te - ts
            logger.info(
                "%r executed in  %2.2f ms " % (method.__name__, (te - ts) * 1000)
            )
            logger.info(f"""{str(datetime.timedelta(seconds=duration))}""")
        return result

    return timed


def parse_kv_pairs_two(text):
    try:
        tokenizer = shlex.shlex(text, posix=True)
    except Exception:
        raise
    tokenizer.commenters = ""
    tokenizer.whitespace_split = True
    tokenizer.whitespace = " "
    result = {}
    try:
        for token in tokenizer:
            if "=" in token:
                logger.debug(token)
                result.update(dict(x.split("=", 1) for x in token.split(",")))
    except ValueError:
        error = tokenizer.token.splitlines()[0]
        logger.debug("parsing problem tokenzer leader: " + tokenizer.error_leader())
        logger.debug("partsing problem text: " + text)

    return result


def get_csv_handle(output_filename, fieldnames):
    csv_file = open(output_filename, "w")
    csv_writer = csv.DictWriter(
        csv_file, delimiter=",", fieldnames=fieldnames, quoting=csv.QUOTE_NONNUMERIC
    )
    return csv_writer


def known_regexes(want_to_match):
    kr = {
        "mac_address": """/^([0-9A-F]{2}[-:]){5}[0-9A-F]{2}$/i""",
        "numbers": """r'\d+""",
    }
    return kr[want_to_match]


def get_filesize(path):
    return pathlib.Path(path).stat().st_size


def strip_regex(string_to_wipe, pattern_to_wipe=r"\d+"):
    logger.debug(f"""Original: {string_to_wipe}""")
    wiped_string = re.sub(pattern_to_wipe, "", string_to_wipe)
    logger.debug(f"""Cleaned of ({pattern_to_wipe}): {wiped_string}""")
    return wiped_string


def wipe_numbers_from_string(string_to_wipe, pattern_to_wipe=r"\d+"):
    logger.debug(f"""Original: {string_to_wipe}""")
    wiped_string = re.sub(pattern_to_wipe, "", string_to_wipe)
    logger.debug(f"""Cleaned of: ({pattern_to_wipe}) ({wiped_string})""")
    return wiped_string


def wipe_64charguids_from_string(
    string_to_wipe, pattern_to_wipe=r"[\-@0-9a-fA-F']{24,64}"
):
    logger.debug(f"""Original: {string_to_wipe}""")
    wiped_string = re.sub(pattern_to_wipe, "", string_to_wipe)
    logger.debug(f"""Cleaned of: ({pattern_to_wipe}) {wiped_string}""")
    return wiped_string


def wipe_guids_from_string(
    string_to_wipe,
    pattern_to_wipe=r"[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}",
):
    logger.debug(f"""Original: {string_to_wipe}""")
    wiped_string = re.sub(pattern_to_wipe, "", string_to_wipe)
    logger.debug(f"""Cleansed: {wiped_string}""")
    return wiped_string


def fix_syslog_date(original_date, base_year=""):
    """
    `original_date='Aug 15 08:38:22`

    Look at the date format. There is no year!

    Oh it gets worse.

    If it's the first 1-9 days of the month:

    ```
    Aug  5 08:38:22
    ```

    Two spaces to trap the unwary.
    """
    original_date = " ".join(original_date.split())
    (m, d, t) = original_date.split(" ")

    if base_year:
        iso_year = base_year
        logger.debug(f"""passed in via base-year: {iso_year}""")
    else:
        base_date_today = datetime.datetime.now()
        iso_year = base_date_today.year
        logger.debug(f"""defaulting to year: {iso_year}""")

    real_date = f"""{iso_year} {m} {d} {t}"""
    real_datetime_obj = datetime.datetime.strptime(real_date, "%Y %b %d %H:%M:%S")
    rd = real_datetime_obj.isoformat()
    return (real_date, rd, real_datetime_obj)


