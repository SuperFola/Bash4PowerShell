#!/usr/bin/env python3

__version__ = "0.0.2"

import os
import sys
import argparse
import shutil
import utils


def remove(path: str, recursive: bool = False):
    try:
        if recursive:
            if not os.path.isdir(path):
                utils.log_error("rm", f"failed to remove '{path}': Not a directory")
                return 1
            shutil.rmtree(path)
        else:
            os.remove(path)
    except FileNotFoundError:
        utils.log_error("rm", f"failed to remove '{path}': No such file or directory")
        return 1
    except OSError:
        utils.log_error("rm", f"failed to remove '{path}': Directory not empty")
        return 1
    else:
        return 0


def rmdir(path: str):
    if not os.path.isdir(path):
        utils.log_error("rm", f"failed to remove '{path}': Not a directory")
        return 1

    try:
        os.rmdir(path)
    except FileNotFoundError:
        utils.log_error("rm", f"failed to remove '{path}': No such file or directory")
        return 1
    except OSError:
        utils.log_error("rm", f"failed to remove '{path}': Directory not empty")
        return 1
    else:
        return 0


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

    if args.version:
        print(f"rm (Python alias mimicking Bash rm) {__version__}")
        return 0

    code = 0

    if args.dir:
        if args.I:
            # interactive one time
            count = len(args.files)
            recur = " recursively" if args.recursive else ""
            question = input(
                f"rm: remove {count} argument{utils.plural(count)}{recur}?"
            )

            if question.lower() not in utils.VALID:
                code = 1
            else:
                for file in args.files:
                    errcode = (
                        remove(file, args.recursive) if args.recursive else rmdir(file)
                    )
                    if errcode != 0:
                        code = errcode
        else:

            def work(files, interactive: bool = False, recursive: bool = False):
                nonlocal code

                for file in files:
                    if interactive and not recursive:
                        question = input(f"rm: remove directory '{file}'? ")
                        if question.lower() not in utils.VALID:
                            continue

                    if interactive:
                        question = input(f"rm: descend into directory '{file}'? ")
                        if question.lower() in utils.VALID:
                            work(list(os.scandir(file)), interactive, recursive)
                    else:
                        errcode = rmdir(file)
                    if errcode != 0:
                        code = errcode

            work(args.files, args.i, args.recursive)
    elif args.recursive and not args.I and not args.i:
        for file in args.files:
            errcode = remove(file, True)
            if errcode != 0:
                code = errcode
                if not args.force:
                    break
    else:
        utils.log_error("rm", f"unhandled option combination: {args}")
        code = -1

    return code


if __name__ == "__main__":
    sys.exit(main())
