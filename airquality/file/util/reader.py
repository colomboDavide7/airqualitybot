#################################################
#
# @Author: davidecolombo
# @Date: gio, 21-10-2021, 11:20
# @Description: this script defines a function that takes the file path as argument and checks both if the file exists
#               and if it is a valid file path;
#               Then, the function open the file, read it and closes the stream before return the content.
#
#################################################
import os
from typing import Generator


def open_read_close_file(path: str) -> str:
    exit_if_path_does_not_exists_or_is_not_file(path=path, caller_name=open_read_close_file.__name__)
    with open(path, "r") as f:
        text = f.read()
    return text


def open_readlines_close_file(path: str) -> Generator[str, None, None]:
    exit_if_path_does_not_exists_or_is_not_file(path=path, caller_name=open_readlines_close_file.__name__)
    file_ref = open(path, "r")
    for line in file_ref:
        yield line
    file_ref.close()


def exit_if_path_does_not_exists_or_is_not_file(path: str, caller_name: str):
    err_msg = f"{caller_name}(): bad path => "
    if not os.path.exists(path):
        raise SystemExit(f"{err_msg} resource at: '{path}' does not exists")
    elif not os.path.isfile(path):
        raise SystemExit(f"{err_msg} resource at: '{path}' is not a file")
