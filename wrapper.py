#!/usr/bin/env python
"""
wrapper.py


"""
__title__ = "wrapper.py"
__version__ = "0.0.1"
__author__ = "Vincent Ricci (vricci)"
__copyright__ = "Copyright (c) 2018-2023 Cisco Systems. All rights reserved."
__credits__ = ""
__maintainer__ = "Vincent Ricci"
__email__ = "vricci@cisco.com"
__status__ = "development"

import os
import logging
import argparse
from pathlib import Path
import sys


# Define global variable logger
logger = logging.getLogger(os.path.basename(__file__))
logger.setLevel(logging.DEBUG)

LOG_FORMAT = (
    "%(asctime)-23s - %(levelname)-8s - %(filename)-15s:%(funcName)-30s %(message)-25s"
)
# replace the extension with .log for the LOGFILE full path
LOG_FILE = os.path.splitext(__file__)[0] + ".log"
LOG_MAXSIZE = 2000000
LOG_COUNT = 10

# Create handlers
c_handler = logging.StreamHandler()
c_handler.setLevel(logging.WARNING)
f_handler = logging.FileHandler(LOG_FILE)
f_handler.setLevel(logging.DEBUG)
c_format = logging.Formatter(LOG_FORMAT)
f_format = c_format
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

logger.addHandler(c_handler)
logger.addHandler(f_handler)


def main(input: str, output: str, list: bool):
    logger.debug("debug example")
    logger.info("info example")
    logger.warning("warning example")
    print(os.path.basename(__file__))


if __name__ == "__main__":
    file = os.path.basename(__file__)
    print(f"\nexecuting {file} as a module...")

    # CLI argument Parsing
    parser = argparse.ArgumentParser(
        prog="wrapper", description="wrap commands read from file"
    )
    parser.add_argument(
        "--debug",
        "-d",
        action="store_true",
        default=False,
        help="enable debug",
    )
    parser.add_argument(
        "--list",
        "-l",
        action="store_true",
        default=False,
        help="list commands from input file. (Default: False)",
    )
    parser.add_argument(
        "--mode",
        "-m",
        choices=["w", "a"],
        default="w",
        help="syslog file mode ('w' or 'a'). (default: 'w')",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default="wrapped_clis.txt",
        const="wrapped_clis.txt",
        nargs="?",
        help="target file where to save wrapped commands",
    )

    parser.add_argument(
        "--input",
        "-i",
        type=str,
        default="clis.txt",
        const="clis.txt",
        nargs="?",
        help="input files containing show commands",
    )

    args = parser.parse_args()

    try:
        if args.debug:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)

        # Clear log files as needed
        if args.mode == "w" and os.path.exists(LOG_FILE):
            parent_dir = Path(LOG_FILE).parent
            logs = [
                os.path.join(parent_dir, f)
                for f in os.listdir(parent_dir)
                if ".log" in f
            ]
            print("\ndeleting logfile(s)\n")
            for log in logs:
                print("\t%r" % log)
                with open(log, mode="w", encoding="UTF-8") as f:
                    f.truncate(0)

        input = str(args.input)
        output = str(args.output)
        list = bool(args.list)

        logger.info("--------- BEGIN %s -------", file)
        main(
            input,
            output,
            list,
        )

    except ValueError as err:
        logger.exception(err)
        logger.warning("Value Error...exiting")
        sys.exit()
    except KeyboardInterrupt as err:
        logger.exception(err)
        logger.warning("KeyboardInterrupt... exiting")
        sys.exit()
    finally:
        logger.info("-------- END %s --------", file)
