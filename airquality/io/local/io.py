#################################################
#
# @Author: davidecolombo
# @Date: gio, 21-10-2021, 11:20
# @Description: this script defines a class for Input/Output operations.
#
#################################################
from airquality.core.constants.shared_constants import EXCEPTION_HEADER


class IOManager:

    @staticmethod
    def open_read_close_file(path: str) -> str:
        f = None
        try:
            f = open(path, "r")
            text = f.read()
        except Exception as ex:
            raise SystemExit(f"{EXCEPTION_HEADER} {IOManager.__name__}: bad I/O => {ex!s}")
        finally:
            if f:
                f.close()
        return text
