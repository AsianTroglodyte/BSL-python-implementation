#!/usr/bin/env python3
"""entry point of the BSL interpreter"""
from typing import List
import sys


def entry_point(args: List[str]):
    """Entry point of program."""

    list_len = len(args)

    if list_len == 1:
        run_file(args[0])
    elif list_len == 0:
        run_repl()
    else:
        print("Error: invalid number of arguments")


def run_file(file_name: str):
    """Run BSL program in a file from specified file path."""
    try:
        with open(file_name, "r") as f:
            content = f.read()
            for char in content:
                print(char, end="")
    except FileNotFoundError:
        print(f"file \"{file_name}\" was not found")


def run_repl():
    """Start up a REPL."""
    while True:
        user_input = input("> ")

        if (user_input == ""):
            break

        print(user_input)


if __name__ == '__main__':
    args = sys.argv[1:]

    entry_point(args)
