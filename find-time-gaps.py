#!/usr/bin/env python3

"""
find-time-gaps.py - this can be used to find gaps (or reversals) in timestamps in a CSV file.

“Lord Cut-Glass, in his kitchen full of time, squats down alone to a dogdish, marked Fido, 
of peppery fish-scraps and listens to the voices of his sixty-six clocks, one for each year of his loony age, 
and watches, with love, their black-and-white moony loudlipped faces tocking the earth away: slow clocks, 
quick clocks, pendulumed heart-knocks, china, alarm, grandfather, cuckoo; clocks shaped like Noah's whirring Ark,
clocks that bicker in marble ships, clocks in the wombs of glass women, hourglass chimers, tu-wit-tuwoo clocks, 
clocks that pluck tunes, Vesuvius clocks all black bells and lava, Niagara clocks that cataract their ticks, 
old time weeping clocks with ebony beards, clocks with no hands for ever drumming out time 
without ever knowing what time it is. His sixty-six singers are all set at different hours. 

Lord Cut-Glass lives in a house and a life at siege. Any minute or dark day now, 
the unknown enemy will loot and savage downhill, but they will not catch him napping. 
Sixty-six different times in his fish-slimy kitchen ping, strike, tick, chime, and tock.”

Under Milk Wood, Dylan Thomas
"""

__version__ = "0.1.0"


import sys
import argparse
import logging
import logging.config
import pandas as pd

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


def main(args):
    logger = logging.getLogger("find-time-gaps")
    logger.setLevel(args.loglevel)

    logger.info(f"""reading {args.filename}""")
    logger.info(f"""acting on {args.column_name}""")
    logger.info(f"""search for gaps of {args.gap}""")
    df = pd.read_csv(args.filename)
    logger.debug(f"""\n{df.head()}""")

    seconds_per_day = 86400
    values_to_eliminate = seconds_per_day - args.tolerance

    df[args.column_name] = pd.to_datetime(df[args.column_name], errors="coerce")
    df.dropna(inplace=True, subset=[args.column_name])
    logger.debug(df[args.column_name])
    df["time_difference"] = df[args.column_name].diff().dt.total_seconds()
    df["longer_gap"] = (df[args.column_name].diff()).dt.total_seconds() >= args.gap

    logger.info("** This section contains locations of detected gaps:***")
    logger.info(f"""*** These values will be removed {values_to_eliminate} ***""")

    result_frame = df[df["time_difference"] > args.gap][
        ["line_number", "time_difference", "longer_gap"]
    ]

    result_frame2 = result_frame[
        result_frame["time_difference"] != values_to_eliminate
    ][["line_number", "time_difference", "longer_gap"]]

    logger.info(f"""\n{result_frame2.to_markdown(index=False)}""")

    logger.info(f"""\n{result_frame.to_markdown(index=False)}""")

    if args.output_format.lower() == "markdown":
        print(f"""\n{result_frame.to_markdown(index=False)}""")
    elif args.output_format.lower() == "csv":
        print(f"""\n{result_frame.to_csv(index=False)}""")
    else:
        print(f"""\n{result_frame.to_string(index=False)}""")


if __name__ == "__main__":
    """This is executed when run from the command line"""

    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="a csv to chomp.")
    parser.add_argument("column_name", help="the column name of the date to evaluate")
    parser.add_argument("-f", "--flag", action="store_true", default=False)
    parser.add_argument(
        "-g", "--gap", action="store", dest="gap", type=int, default=300
    )
    parser.add_argument(
        "-t", "--tolerance", action="store", dest="tolerance", type=int, default=1
    )

    # Optional verbosity counter (eg. -v, -vv, -vvv, etc.)
    parser.add_argument(
        "-v", "--verbose", action="count", default=0, help="Verbosity (-v, -vv, etc)"
    )

    # Specify output of "--version"
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__),
    )

    parser.add_argument(
        "--output-format",
        action="store",
        dest="output_format",
        default="string",
        help="--output-format  output format to use: string, csv, markdown are valid",
    )

    parser.add_argument(
        "-d",
        "--debug",
        action="store_const",
        dest="loglevel",
        const=logging.DEBUG,
        default=logging.WARNING,
        help="debug(-d, --debug, etc)",
    )

    args = parser.parse_args()
    main(args)
