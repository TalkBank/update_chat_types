"""
pytest
"""

import shutil
import tempfile
import filecmp
import os.path

from update_chat_types import (
    has_types_header,
    collect_chat_types,
    read_types,
    updated_contents,
    update_chat_types,
)

OLD_CHAT_DIR = "test-data/old"
EXPECTED_CHAT_DIR = "test-data/new"


def test_collect_chat_types():
    """
    Make sure types info calculated properly.
    """
    (types_dirs, types_dict) = collect_chat_types(OLD_CHAT_DIR)
    assert types_dirs == set(["test-data/old/sub0", "test-data/old/sub0/sub1"])
    assert types_dict == {
        "test-data/old": None,
        "test-data/old/side": None,
        "test-data/old/sub0": "test-data/old/sub0",
        "test-data/old/sub0/sub1": "test-data/old/sub0/sub1",
        "test-data/old/sub0/sub1/sub2": None,
    }


def test_update_old_types():
    types_header = "@Types:\ttop1, top2, top3"
    contents = """@Begin
@Comment:\tcomment
@Types:\told1, old2, old3
*CHI:\tword .
*CHI:\tword word .
@End
"""
    new_contents = """@Begin
@Comment:\tcomment
@Types:\ttop1, top2, top3
*CHI:\tword .
*CHI:\tword word .
@End
"""
    assert has_types_header(contents)
    assert updated_contents(contents, types_header) == new_contents


def test_insert_new_types():
    types_header = "@Types:\ttop1, top2, top3"
    contents = """@Begin
@Comment:\tcomment
*CHI:\tword .
*CHI:\tword word .
@End
"""
    new_contents = """@Begin
@Comment:\tcomment
@Types:\ttop1, top2, top3
*CHI:\tword .
*CHI:\tword word .
@End
"""
    assert not (has_types_header(contents))
    assert updated_contents(contents, types_header) == new_contents


def test_read_types():
    """
    Make sure parsing of 0types.txt file works.
    """
    types_info = read_types(os.path.join(OLD_CHAT_DIR, "sub0", "0types.txt"))
    assert types_info == "@Types:\ttop1, top2, top3"


def are_dir_trees_equal(dir1: str, dir2: str) -> bool:
    """
    From https://stackoverflow.com/a/6681395.

    Compare two directories recursively. Files in each directory are
    assumed to be equal if their names and contents are equal.

    @param dir1: First directory path
    @param dir2: Second directory path

    @return: True if the directory trees are the same and
        there were no errors while accessing the directories or files,
        False otherwise.
    """
    dirs_cmp = filecmp.dircmp(dir1, dir2)
    if dirs_cmp.left_only or dirs_cmp.right_only or dirs_cmp.funny_files:
        return False
    (_, mismatch, errors) = filecmp.cmpfiles(
        dir1, dir2, dirs_cmp.common_files, shallow=False
    )
    if mismatch or errors:
        return False
    for common_dir in dirs_cmp.common_dirs:
        new_dir1 = os.path.join(dir1, common_dir)
        new_dir2 = os.path.join(dir2, common_dir)
        if not are_dir_trees_equal(new_dir1, new_dir2):
            return False
    return True


def assert_dir_trees_equal(dir1: str, dir2: str):
    """
    Based on https://stackoverflow.com/a/6681395.

    Compare two directories recursively. Files in each directory are
    assumed to be equal if their names and contents are equal.

    @param dir1: First directory path
    @param dir2: Second directory path
    """
    dirs_cmp = filecmp.dircmp(dir1, dir2)
    assert dirs_cmp.left_only == []
    assert dirs_cmp.right_only == []
    assert dirs_cmp.funny_files == []

    (_, mismatch, errors) = filecmp.cmpfiles(
        dir1, dir2, dirs_cmp.common_files, shallow=False
    )
    assert mismatch == []
    assert errors == []
    for common_dir in dirs_cmp.common_dirs:
        new_dir1 = os.path.join(dir1, common_dir)
        new_dir2 = os.path.join(dir2, common_dir)
        assert_dir_trees_equal(new_dir1, new_dir2)


def test_update_chat_types():
    """Copy test CHAT dir to a temporary place, run the updater,
    and compare with the expected result.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        copied_chat_dir = os.path.join(temp_dir, "old")
        shutil.copytree(OLD_CHAT_DIR, copied_chat_dir)
        num_updated = update_chat_types(copied_chat_dir)
        assert_dir_trees_equal(copied_chat_dir, EXPECTED_CHAT_DIR)
        assert num_updated == 8
