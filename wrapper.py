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

import logging
import os,sys
import argparse

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



def main(input:str):
    logger.debug("all good")
    logger.info("start")
    logger.warning("warning")
    print(os.path.basename(__file__))

if __name__ == "__main__":
    file = os.path.basename(__file__)
    print(f"\nexecuting {file} as a module...")

    # CLI argument Parsing
    parser = argparse.ArgumentParser(
        prog="wrapper", description="wrap clis"
    )
    # parser.add_argument(
    #     "--archive",
    #     "-a",
    #     type=str,
    #     default=TEST_ARCHIVE,
    #     const=TEST_ARCHIVE,
    #     nargs="?",
    #     help="path to archive to decode. (Default: %r)" % TEST_ARCHIVE,
    # )
    # parser.add_argument(
    #     "--clean",
    #     "-c",
    #     action="store_true",
    #     default=False,
    #     help="clean directory folder",
    # )
    parser.add_argument(
        "--debug",
        "-d",
        action="store_true",
        default=False,
        help="enable debug",
    )
    # parser.add_argument(
    #     "--list",
    #     "-l",
    #     action="store_true",
    #     default=False,
    #     help="Select from list. (Default: False)",
    # )
    # parser.add_argument(
    #     "--mode",
    #     "-m",
    #     choices=["w", "a"],
    #     default="w",
    #     help="syslog file mode ('w' or 'a'). (default: 'w')",
    # )
    # parser.add_argument(
    #     "--released",
    #     "-r",
    #     action="store_true",
    #     default=False,
    #     help="list released decoders. (Default: False)",
    # )
    parser.add_argument(
        "--input",
        "-i",
        type=str,
        default="clis.txt",
        const="clis.txt",
        nargs="?",
        help="input file where commands are saved",
    )
    # parser.add_argument(
    #     "--store",
    #     "-o",
    #     type=str,
    #     default=DECODERS_STORE,
    #     const=DECODERS_STORE,
    #     nargs="?",
    #     help="store containing all supported BU decoders. Use '-r' to list content (Default: %r)"
    #     % DECODERS_STORE,
    # )
    # parser.add_argument(
    #     "--table",
    #     "-t",
    #     type=str,
    #     default=LATEST_DECODER_TABLE,
    #     const=LATEST_DECODER_TABLE,
    #     nargs="?",
    #     help="decoder table. (Default: %r)" % LATEST_DECODER_TABLE,
    # )
    # parser.add_argument(
    #     "--use-folder",
    #     "-u",
    #     action="store_true",
    #     default=False,
    #     help="Assign decoder from folder. (Default: False)",
    # )
    # parser.add_argument(
    #     "--folder",
    #     "-f",
    #     type=str,
    #     default=ACTIVE_DECODER_DIR,
    #     const=ACTIVE_DECODER_DIR,
    #     nargs="?",
    #     help="folder containing active decoder and table. (Default: %r)"
    #     % ACTIVE_DECODER_DIR,
    # )

    args = parser.parse_args()

    try:

        if args.debug:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)

        # # Clear log files as needed
        # if args.mode == "w" and os.path.exists(LOG_FILE):
        #     parent_dir = Path(LOG_FILE).parent
        #     logs = [
        #         os.path.join(parent_dir, f)
        #         for f in os.listdir(parent_dir)
        #         if ".log" in f
        #     ]
        #     print("\ndeleting logfile(s)\n")
        #     for log in logs:
        #         print("\t%r" % log)
        #         with open(log, mode="w", encoding="UTF-8") as f:
        #             f.truncate(0)

        input = str(args.input)
        # output = str(args.output)

        main(
            input,
        )

    except KeyboardInterrupt as err:
        logger.exception(err)
        logger.warning("KeyboardInterrupt... exiting")
        sys.exit()

    finally:
        logger.info("-------- END %s --------", file)