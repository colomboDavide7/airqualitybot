######################################################
#
# Author: Davide Colombo
# Date: 23/12/21 10:12
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from time import perf_counter


class ProgramTimer(object):

    def __init__(self):
        self._started_at = 0
        self._ended_at = 0
        self._elapsed = 0

    def __enter__(self):
        self._started_at = perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._ended_at = perf_counter()
        print(f"elapsed: {self.elapsed}s")

    @property
    def elapsed(self) -> float:
        if not self._elapsed:
            if not self._started_at:
                raise ValueError(f"{type(self).__name__} expected the timer to be started before compute the elapsed time")
            if not self._ended_at:
                raise ValueError(f"{type(self).__name__} expected the timer to be stopped before compute the elapsed time")
            self._elapsed = self._ended_at - self._started_at
        return self._elapsed

    def __repr__(self):
        return f"{type(self).__name__}(started_at={self._started_at}s, ended_at={self._ended_at}s, elapsed={self.elapsed}s)"
