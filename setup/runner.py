#################################################
#
# @Author: davidecolombo
# @Date: dom, 24-10-2021, 20:36
# @Description: this script defines the main function for the 'setup' module

#               This module is used for loading for the first time the sensor's data to the
#
#################################################
import sys
from typing import List
from airquality.io.io import IOManager
from airquality.parser.file_parser import FileParserFactory
from airquality.api.api_request_adapter import APIRequestAdapter
from airquality.api.url_querystring_builder import URLQuerystringBuilder


DEBUG_HEADER = "[DEBUG]:"
SETUP_FILE = "properties/setup.json"
USAGE = "USAGE: python -m setup [-d or --debug] personality"
VALID_PERSONALITIES = 'purpleair'
DEBUG_MODE = False
PERSONALITY = None


def parse_sys_argv(args: List[str]):

    global DEBUG_MODE
    global PERSONALITY
    is_personality_set = False

    for arg in args:
        if arg in ("-d", "--debug"):
            DEBUG_MODE = True
        elif arg in VALID_PERSONALITIES and not is_personality_set:
            PERSONALITY = arg
            is_personality_set = True
        else:
            print(f"{parse_sys_argv.__name__}(): ignoring invalid option '{arg}'")

    if not is_personality_set:
        raise SystemExit(f"{parse_sys_argv.__name__}(): missing personality argument. \n{USAGE}")


def main():
    """This function is the entry point for the 'setup' module.

    The module allows to set up all the information associated to the sensors and add them to the database."""

    args = sys.argv[1:]
    if args:
        parse_sys_argv(args)

    print(f"{DEBUG_HEADER} personality = {PERSONALITY}")
    print(f"{DEBUG_HEADER} debug       = {DEBUG_MODE}")

    try:
        print(20*'-' + " START THE PROGRAM " + 20*'-')

        # TRY TO READ FILE
        raw_text = IOManager.open_read_close_file(path = SETUP_FILE)
        # if DEBUG_MODE:
        #     print(raw_text)

        # GET THE FILE PARSER
        parser = FileParserFactory.file_parser_from_file_extension(file_extension = SETUP_FILE.split('.')[-1])
        if DEBUG_MODE:
            print(DEBUG_HEADER + str(parser))

        # TRY TO PARSE FILE RAW TEXT
        parsed_content = parser.parse(raw_string = raw_text)
        # if DEBUG_MODE:
        #     print(parsed_content)

        # MAKE API REQUEST ADAPTER
        api_adapter = APIRequestAdapter(parsed_content[f"{PERSONALITY}"]["api_address"])

        # TRY TO BUILD QUERYSTRING FROM API PARAMETERS
        querystring = URLQuerystringBuilder.PA_querystring_from_fields(api_param = parsed_content[f"{PERSONALITY}"])
        if DEBUG_MODE:
            print(DEBUG_HEADER + querystring)

        # TRY TO FETCH DATA FROM PURPLE AIR API
        raw_string = api_adapter.fetch(query_string = querystring)
        # if DEBUG_MODE:
        #     print(raw_string)

        # GET JSON PARSER
        parser = FileParserFactory.file_parser_from_file_extension(file_extension = 'json')

        # TRY TO PARSE API REQUEST
        parsed_string = parser.parse(raw_string = raw_string)
        # if DEBUG_MODE:
        #     print(DEBUG_HEADER + str(parsed_string))

        



        print(20 * '-' + " PROGRAMS END SUCCESSFULLY " + 20 * '-')
    except Exception as ex:
        print(str(ex))
        if isinstance(ex, SystemExit):
            sys.exit(1)
















