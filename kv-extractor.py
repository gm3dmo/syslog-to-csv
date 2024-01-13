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
import json

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

    lines = log_entry.splitlines()

    results = {}
    for i, line in enumerate(lines):
        r = parse_kv_pairs_two(log_entry)
        results.update(r)

    logger.debug(f"""keys: {results.keys()}""")
    logger.debug(f"""length keys: {len(results.keys())}""")

    print(json.dumps(list(results.keys())))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--extension", action="store", dest="extension", default="c")

    parser.add_argument(
        "-l",
        "--loglevel",
        action="store",
        dest="loglevel",
        default="info",
        help="Set the log level",
    )

    args = parser.parse_args()

    main(args)
