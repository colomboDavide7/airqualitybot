#################################################
#
# @Author: davidecolombo
# @Date: gio, 21-10-2021, 11:20
# @Description: this script defines a class for Input/Output operations.
#
#################################################
import os


def open_read_close_file(path: str) -> str:
    """Function that checks if the 'path' point to an existing resource and if it is, it checks if the resource is
    a file or not: in the latter case a SystemExit exception is raised. """

    err_msg = ""
    if not os.path.exists(path):
        err_msg += f"{open_read_close_file.__name__} bad file path => '{path}' does not exists"
    elif not os.path.isfile(path):
        err_msg += f"{open_read_close_file.__name__} bad file path => '{path}' not a file"

    if err_msg:
        raise SystemExit(err_msg)

    # Open the file, read the text and close the file.
    with open(path, "r") as f:
        text = f.read()
    f.close()
    return text
