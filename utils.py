#!/usr/bin/env python3

__version__ = "0.0.1"

VALID = ("y", "yes")


def log_error(command: str, msg: str):
    print(f"{command}: {msg}")


def plural(count: int):
    return "s" if count > 1 else ""
