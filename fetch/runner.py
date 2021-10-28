#################################################
#
# @Author: davidecolombo
# @Date: lun, 18-10-2021, 12:29
# @Description: this script defines the functions for parsing application arguments and 'main()'.
#
#################################################
import sys
import time
from typing import List
from airquality.bot.fetch_bot import FetchBotFactory
from airquality.constants.shared_constants import FETCH_USAGE, VALID_PERSONALITIES, DEBUG_HEADER
import airquality.constants.system_constants as sc


def parse_sys_argv(args: List[str]):

    if args[0] in ("--help", "-h"):
        print(FETCH_USAGE)
        sys.exit(0)

    is_personality_set = False

    for arg in args:
        if arg in ("-d", "--debug"):
            sc.DEBUG_MODE = True
        elif not is_personality_set and arg in VALID_PERSONALITIES:
            sc.PERSONALITY = arg
            is_personality_set = True
        else:
            print(f"{parse_sys_argv.__name__}: ignore invalid option '{arg}'.")

    if not is_personality_set:
        raise SystemExit(f"{parse_sys_argv.__name__}(): missing required bot personality.")


################################ MAIN FUNCTION ################################
def main():

    args = sys.argv[1:]
    if not args:
        print(FETCH_USAGE)
        sys.exit(1)

    parse_sys_argv(args)
    print(f"{DEBUG_HEADER} personality = {sc.PERSONALITY}")
    print(f"{DEBUG_HEADER} debug       = {sc.DEBUG_MODE}")

    try:
        print(20 * '-' + " START THE PROGRAM " + 20 * '-')

        start_time = time.perf_counter()
        fetch_bot = FetchBotFactory().create_fetch_bot(bot_personality = sc.PERSONALITY)
        fetch_bot.run()
        end_time = time.perf_counter()
        print(f"{DEBUG_HEADER} elapsed time: {end_time - start_time}")

        print(20 * '-' + " PROGRAMS END SUCCESSFULLY " + 20 * '-')

    except SystemExit as ex:
        print(str(ex))
        sys.exit(1)
