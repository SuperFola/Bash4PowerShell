#!/usr/bin/env python3

__version__ = "0.0.1"

import os
import sys
import argparse
import utils


def main():
    parser = argparse.ArgumentParser(
        prog="rm",
        description="Remove (unlink) the FILE(s)",
    )
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="ignore nonexistent files and arguments, never prompt",
    )
    parser.add_argument(
        "-i",
        action="store_true",
        help="prompt before every removal",
    )
    parser.add_argument(
        "-I",
        action="store_true",
        help="prompt once before removing more than three files, "
        "or when removing recursively; less intrusive than -i, "
        "while still giving protection against most mistakes",
    )
    parser.add_argument(
        "-r",
        "-R",
        "--recursive",
        action="store_true",
        help="remove directories and their contents recursively",
    )
    parser.add_argument(
        "-d",
        "--dir",
        action="store_true",
        help="remove empty directories",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="explain what is being done",
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help="output version information and exit",
    )
    parser.add_argument(
        "files",
        metavar="FILE",
        nargs="+",
    )

    args = parser.parse_args()
    print(args)

    if args.version:
        print(f"rm (Python alias mimicking Bash rm) {__version__}")
        return 0

    if args.dir:
        for file in args.files:
            try:
                os.rmdir(file)
            except FileNotFoundError:
                utils.log_error("rm", f"failed to remove '{file}': No such file or directory")
            except OSError:
                utils.log_error("rm", f"failed to remove '{file}: Directory not empty")

            if not os.path.isdir(file):
                utils.log_error("rm", f"failed to remove '{file}': Not a directory")
                return -1
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
