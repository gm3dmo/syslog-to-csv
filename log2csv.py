#!/usr/bin/env python

import re
import csv
import time
import json
import shlex
import pathlib
import datetime
import logging
import logging.config

logger = logging.getLogger("log2csv")


def is_gzipped(path):
    if  path.suffix == ".gz":
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
