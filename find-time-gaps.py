#!/usr/bin/env python3

"""
find-time-gaps.py - this can be used to find gaps (or reversals) in timestamps in a CSV file. 
"""

__version__ = "0.1.0"


import sys
import argparse
import logging
import logging.config
from datetime import datetime, timedelta
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

   df[args.column_name] = pd.to_datetime(df[args.column_name], errors='coerce')
   df.dropna(inplace=True, subset=[args.column_name])
   logger.debug(df[args.column_name])
   df['time_difference'] = df[args.column_name].diff().dt.total_seconds()
   df['longer_gap'] = (df[args.column_name].diff()).dt.total_seconds() >= args.gap

   logger.info("** This section contains locations of detected gaps:***")
   logger.info(f"""*** These values will be removed {values_to_eliminate} ***""")

   result_frame = df[df["time_difference"]>args.gap][["line_number","time_difference","longer_gap","line"]]

   result_frame2 = result_frame[result_frame['time_difference']!=values_to_eliminate][["line_number","time_difference","longer_gap","line"]]

   logger.info(f"""\n{result_frame2.to_markdown(index=False)}""")

   logger.info(f"""\n{result_frame.to_markdown(index=False)}""")

   if args.output_format.lower() == "markdown":
       print(f"""\n{result_frame.to_markdown(index=False)}""")
   elif args.output_format.lower() == "csv":
       print(f"""\n{result_frame.to_csv(index=False)}""")
   else:
       print(f"""\n{result_frame.to_string(index=False)}""")

if __name__ == "__main__":
    """ This is executed when run from the command line """

    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="a csv to chomp.")
    parser.add_argument("column_name", help="the column name of the date to evaluate" )
    parser.add_argument("-f", "--flag", action="store_true", default=False)
    parser.add_argument("-g", "--gap", action="store", dest="gap", type=int,default=300)
    parser.add_argument("-t", "--tolerance", action="store", dest="tolerance", type=int,default=1)

    # Optional verbosity counter (eg. -v, -vv, -vvv, etc.)
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Verbosity (-v, -vv, etc)")

    # Specify output of "--version"
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__))

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




