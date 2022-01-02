######################################################
#
# Author: Davide Colombo
# Date: 31/12/21 19:05
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import sys
from airquality.environment import Environment
from airquality.usecase_runner import AddFixedSensorsRunner, AddAtmotubeMeasuresRunner, AddThingspeakMeasuresRunner


class WrongUsageError(Exception):
    """
    An *Exception* that defines the type of error raised when the application is used in the wrong way.
    """

    def __init__(self, cause: str):
        self.cause = cause

    def __repr__(self):
        return f"{type(self).__name__}(cause={self.cause})"


class Application(object):
    """
    An *object* that implements the context manager interface and defines the *main()* method, application entry point.
    All the relevant Exceptions are caught at higher level by this class and logged.
    """

    def __init__(self, env: Environment):
        self.args = sys.argv[1:]
        self.env = env

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type == WrongUsageError:
            print(repr(exc_val))
            print(self.env.program_usage_msg)
            sys.exit(1)

    def main(self):
        """
        The application entry point method.
        """

        if not self.args:
            raise WrongUsageError("expected at least one argument!")

        personality = self.args[0]
        if personality not in self.env.valid_personalities:
            raise WrongUsageError("invalid personality!")

        print(f"RUNNING {personality}...")
        if personality == 'purpleair':
            AddFixedSensorsRunner(env=self.env, personality=personality).run()
        elif personality == 'atmotube':
            AddAtmotubeMeasuresRunner(env=self.env, personality=personality).run()
        elif personality == 'thingspeak':
            AddThingspeakMeasuresRunner(env=self.env, personality=personality).run()
        print("finish!")
