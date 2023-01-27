#!/usr/bin/env python

import re
import csv
import gzip
import time
import json
import shlex
import pathlib
import datetime
import logging
import logging.config
import unicodedata

logger = logging.getLogger("log2csv")


def get_log_type(path):
    log_type = path.stem.split(".")[0]
    return log_type


def create_list_of_files_to_convert(args):
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
            if str(item).endswith(".csv"):
                continue
            if item.name.startswith("syslog"):
                syslog_files.append(item)
                logger.debug(f"{item.name}")

            else:
                log_type = get_log_type(item)
                if log_type in args.log_types:
                
                    table_name = get_table_name(log_type)
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
            if data[log_type]["table_name"]:
                table_name = data[log_type]["table_name"]
            return table_name


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


def main():
    """main"""


if __name__ == "__main__":
    main()
