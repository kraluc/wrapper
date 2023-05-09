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

# Global Variables

DEFAULT_INPUT_FILE = "cli.txt"
DEFAULT_OUTPUT_FILE = f"wrapped_{DEFAULT_INPUT_FILE}"

# Functions


def commands_from_file(filename: str) -> list:
    try:
        # open input file to read commands
        with open(file=filename, mode="r", encoding="UTF-8") as f_read:
            logger.debug("opened %r for reading", filename)
            commands = f_read.readlines()
        # Remove end of line characters
        commands = [cli.strip() for cli in commands]
        logger.info("read command(s): %r", commands)
        return commands
    except FileNotFoundError as err:
        # logger.exception(err)
        logger.warning("File Not Found: %r", filename)
        raise ValueError


def header(msg: str, sep: str = "="):
    print(msg)
    print("=" * len(msg))
    print()


def wrapper(cli: str) -> list:
    """
    wrapper: generate a command string, add a timestamp and redirect the output to file
    """
    # first line is a comment showing the command name
    template = "%s >> $(SWITCHNAME)-debugs.txt" + "\n"
    wrapped_commands = template % 'echo "### %s"' % cli
    wrapped_commands += template % "show clock"
    wrapped_commands += template % cli
    return wrapped_commands


def wite_commands_to_file(commands: list, output: str):
    try:
        commands = list(commands)
        with open(file=output, mode="w", encoding="UTF-8") as f_write:
            logger.debug("opened %r for writing", output)
            f_write.writelines(commands)
        logger.info("command(s) written to: %r", output)
    except FileNotFoundError as err:
        logger.exception(err)
        raise ValueError


def print_commands(commands: list):
    for cli in commands:
        print(cli)


def main(input: str, output: str):
    """main function"""
    # Read input commands
    commands = commands_from_file(input)
    msg = "\ncommands read from %s:" % input
    header(msg)
    print_commands(commands)
    print()

    # Generate wrapped commands
    wrapped_commands = [wrapper(cli) for cli in commands]

    msg = "wrapped commands:"
    header(msg)
    print("\n".join(wrapped_commands))
    print()

    # Display commands and write them to file
    wite_commands_to_file(wrapped_commands, output)
    print("\nwrapped commands saved to %r" % output)


if __name__ == "__main__":
    file = os.path.basename(__file__)
    logfile = file.replace(".py", ".log")
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
        "--input",
        "-i",
        type=str,
        default=DEFAULT_INPUT_FILE,
        const=DEFAULT_INPUT_FILE,
        nargs="?",
        help="file containing show commands (Default: %r)." % DEFAULT_INPUT_FILE,
    )
    parser.add_argument(
        "--mode",
        "-m",
        choices=["w", "a"],
        default="w",
        help=f"'a'ppend or over'w'rite logs to '{logfile}'. Default: 'w'",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default=DEFAULT_OUTPUT_FILE,
        const=DEFAULT_OUTPUT_FILE,
        nargs="?",
        help="save output to file. (Default: %r)" % DEFAULT_OUTPUT_FILE,
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
            print("\n\toverwrite existing logfile(s)")
            for log in logs:
                print("\t%r" % log)
                with open(log, mode="w", encoding="UTF-8") as f:
                    f.truncate(0)

        input_file = str(args.input)
        output_file = str(args.output)

        logger.info("--------- BEGIN %s -------", file)
        main(
            input=input_file,
            output=output_file,
        )

    except ValueError as err:
        logger.exception(err)
        logger.warning("Value Error...exiting")
        sys.exit()
    except IOError as err:
        logger.exception(err)
        logger.warning("I/O error: {0}: {1}".format(err.errno, err.strerror))
    except KeyboardInterrupt as err:
        logger.exception(err)
        logger.warning("KeyboardInterrupt... exiting")
        sys.exit()
    finally:
        logger.info("-------- END %s --------", file)
