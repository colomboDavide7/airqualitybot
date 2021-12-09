######################################################
#
# Author: Davide Colombo
# Date: 28/11/21 15:39
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import airquality.command.fetch.atmfact as atm
import airquality.command.fetch.thnkfact as thnk


def get_fetch_factory_cls(command_type: str):
    function_name = get_fetch_factory_cls.__name__
    valid_types = ["atmotube", "thingspeak"]

    if command_type == 'atmotube':
        return atm.AtmotubeFetchFactory
    elif command_type == "thingspeak":
        return thnk.ThingspeakFetchFactory
    else:
        raise SystemExit(f"{function_name}: bad type => VALID TYPES: [{'|'.join(t for t in valid_types)}]")
