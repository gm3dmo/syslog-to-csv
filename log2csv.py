#!/usr/bin/env python


import re
from logzero import logger
import datetime


def known_regexes(want_to_match):
    kr = {
        "mac_address": """/^([0-9A-F]{2}[-:]){5}[0-9A-F]{2}$/i""",
        "numbers": """r'\d+""",
    }
    return kr[want_to_match]


def strip_regex(string_to_wipe, pattern_to_wipe=r"\d+"):
    logger.debug(f"""Original: {string_to_wipe}""")
    wiped_string = re.sub(pattern_to_wipe, "", string_to_wipe)
    logger.debug(f"""Cleansed: {wiped_string}""")
    return wiped_string


def wipe_numbers_from_string(string_to_wipe, pattern_to_wipe=r"\d+"):
    logger.debug(f"""Original: {string_to_wipe}""")
    wiped_string = re.sub(pattern_to_wipe, "", string_to_wipe)
    logger.debug(f"""Cleansed: {wiped_string}""")
    return wiped_string


def wipe_64charguids_from_string(
    string_to_wipe, pattern_to_wipe=r"[\-@0-9a-fA-F']{24,64}"
):
    logger.debug(f"""Original: {string_to_wipe}""")
    wiped_string = re.sub(pattern_to_wipe, "", string_to_wipe)
    logger.debug(f"""Cleansed: {wiped_string}""")
    return wiped_string


def wipe_guids_from_string(
    string_to_wipe,
    pattern_to_wipe=r"[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}",
):
    logger.debug(f"""Original: {string_to_wipe}""")
    wiped_string = re.sub(pattern_to_wipe, "", string_to_wipe)
    logger.debug(f"""Cleansed: {wiped_string}""")
    return wiped_string


def fix_syslog_date(original_date):
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

    x = datetime.datetime.now()
    iso_year = x.year

    real_date = f"""{iso_year} {m} {d} {t}"""
    real_datetime_obj = datetime.datetime.strptime(real_date, "%Y %b %d %H:%M:%S")
    rd = real_datetime_obj.isoformat()
    return (real_date, rd, real_datetime_obj)


if __name__ == "__main__":
    main()
