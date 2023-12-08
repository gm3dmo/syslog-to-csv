#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Your Name"
__version__ = "0.1.0"
__license__ = "MIT"

import sys
import shlex
import logging
import argparse

logger = logging.getLogger(__name__)


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
                logger.debug(f"""token: {token}""")
                key, value = token.split("=", 1)  # Split at the first equal sign only
                result[key] = value
                #result.update(dict(x.split("=", 1) for x in token.split(",",1)))
    except ValueError:
        error = tokenizer.token.splitlines()[0]
        logger.info("parsing problem tokenzer leader: " + tokenizer.error_leader())
        logger.info("partsing problem text: " + text)

    return result



def main(args):
    """ Main entry point of the app """

    loglevel = args.loglevel.upper()
    logging.basicConfig(level=loglevel)
    logger = logging.getLogger(__name__)


    log_entry = sys.stdin.read()

    r = parse_kv_pairs_two(log_entry)
    print(f"""log entry: {log_entry}""")
    print(r)
    print(f"""keys: {r.keys()}""")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--power-config", action="store", dest="power_config", default=".gh-api-examples.conf", help="This is the config file to use to access variables for the power.")
    parser.add_argument("-e", "--extension", action="store", dest="extension", default="c")

    parser.add_argument(
        "--issues",
        action="store",
        dest="number_of_issues",
        default=3,
        help="The number of issues to create.",
    )
    parser.add_argument(
        "-l",
        "--loglevel",
        action="store",
        dest="loglevel",
        default="debug",
        help="Set the log level",
    )

    args = parser.parse_args()

    main(args)
