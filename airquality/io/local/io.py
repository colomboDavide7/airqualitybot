#################################################
#
# @Author: davidecolombo
# @Date: gio, 21-10-2021, 11:20
# @Description: this script defines a class for Input/Output operations.
#
#################################################
import builtins


class IOManager(builtins.object):
    """Class that defines for Input/Output common operations."""

    @staticmethod
    def open_read_close_file(path: str) -> str:
        """Static method that opens, read and closes the file found at 'path' string."""

        f = None
        try:
            f = open(path, "r")
            text = f.read()
        except Exception as ex:
            raise SystemExit(f"{IOManager.__name__}: {str(ex)}")
        finally:
            if f:
                f.close()
        return text
