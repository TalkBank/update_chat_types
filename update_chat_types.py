#!/usr/bin/env python3

from typing import Iterable, Set, Dict, Optional, Tuple

import re
import sys
import os
import click


RE_TYPES_HEADER = re.compile(r"^@Types:.+$", re.MULTILINE)

RE_AT_FIRST_UTTERANCE = re.compile(r"(?=^\*)", re.MULTILINE)


@click.command()
@click.option("--chatdir", required=True, help="CHAT root dir")
def main(chatdir: str):
    """
    Update, in place, CHAT files. Insert or change @Types header in
    each CHAT file, recursively, according to the 0types.txt in the
    same directory.

    May throw Exception if 0types.txt exists but is malformed.
    """
    update_chat_types(chatdir)


def update_chat_types(chatdir: str) -> int:
    """First, collect, parse, and validate all 0types.txt files and make
    note of the dirs they came from.

    Then apply the modifications to all the files.

    Return how many files actually changed.

    May throw Exception if bad 0types.txt file.
    """
    num_updated = 0
    (types_dirs, types_dict) = collect_chat_types(chatdir)

    # Parse all the 0types.txt files.
    types_info: Dict[str, str] = dict(
        (dir, read_types(os.path.join(dir, "0types.txt"))) for dir in types_dirs
    )

    for dir_path, dir_names, file_names in os.walk(chatdir):
        if ".git" in dir_names:
            dir_names.remove(".git")
        for file_name in file_names:
            if file_name.endswith(".cha"):
                types_dir = types_dict[dir_path]
                if types_dir:
                    # There is a relevant types file to use.
                    if update_types_in_file(
                        os.path.join(dir_path, file_name), types_info[types_dir]
                    ):
                        num_updated += 1
    return num_updated


def update_types_in_file(chat_path: str, types_header: str) -> bool:
    """
    Update @Types header in file, if needed.
    Return whether there was a change.
    """
    with open(chat_path, "r", encoding="utf-8") as fin:
        contents = fin.read()
    new_contents = updated_contents(contents, types_header)
    if new_contents is not None:
        with open(chat_path, "w", encoding="utf-8") as fout:
            fout.write(new_contents)
        return True
    else:
        return False


def has_types_header(contents: str) -> bool:
    """Return whether text has a @Types header."""
    return RE_TYPES_HEADER.search(contents) is not None


def updated_contents(contents: str, types_header: str) -> Optional[str]:
    """Return updated contents, if anything changed, else None.
    """
    if has_types_header(contents):
        # Replace all.
        new_contents, num = RE_TYPES_HEADER.subn(types_header, contents)
    else:
        # Replace only at first utterance.
        new_contents, num = RE_AT_FIRST_UTTERANCE.subn(
            types_header + "\n", contents, count=1
        )
    if new_contents != contents:
        return new_contents
    else:
        return None


def read_types(types_path: str) -> str:
    """Parse first line of types file and return it, excluding newline.

    Throw an exception if the line is malformed.
    """
    with open(types_path, "r", encoding="utf-8") as fin:
        for line in fin:
            search = re.search(r"^@Types:\t(\S+), (\S+), (\S+)$", line)
            break
    if search:
        return line.rstrip()
    raise Exception(f"{types_path} has bad @Types line")


def collect_chat_types(chatdir: str) -> Tuple[Set[str], Dict[str, Optional[str]]]:
    """Look for all 0types.txt and return a set of dirs that have them,
    along with a dict mapping each dir to itself or None.
    """
    types_dirs: Set[str] = set()
    # Map from dir to which closest dir has 0types.txt, if any at all.
    types_dict: Dict[str, Optional[str]] = {}
    for dir_path, dir_names, file_names in os.walk(chatdir):
        if ".git" in dir_names:
            dir_names.remove(".git")
        if "0types.txt" in file_names:
            types_dirs.add(dir_path)
            types_dict[dir_path] = dir_path
        else:
            types_dict[dir_path] = None
    return (types_dirs, types_dict)


if __name__ == "__main__":
    main()
