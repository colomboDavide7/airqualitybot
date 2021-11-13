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


def open_read_close_file(path: str) -> str:

    err_msg = f"'{open_read_close_file.__name__}()': bad path => "
    if not os.path.exists(path):
        raise SystemExit(f"{err_msg} resource at: '{path}' does not exists")
    elif not os.path.isfile(path):
        raise SystemExit(f"{err_msg} resource at: '{path}' is not a file")

    # Open the file, read the text and close the file.
    with open(path, "r") as f:
        text = f.read()
    f.close()
    return text
