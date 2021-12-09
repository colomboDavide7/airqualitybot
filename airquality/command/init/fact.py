######################################################
#
# Author: Davide Colombo
# Date: 03/12/21 20:04
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import airquality.command.init.purpfact as purpfact
import airquality.command.initsrv.geonamesfact as geofact


def get_init_factory_cls(command_type: str):
    function_name = get_init_factory_cls.__name__
    valid_types = ["purpleair", "geonames"]

    if command_type == 'purpleair':
        return purpfact.PurpleairInitFactory
    elif command_type == "geonames":
        return geofact.GeonamesInitCommandFactory
    else:
        raise SystemExit(f"{function_name}: bad type => VALID TYPES: [{'|'.join(t for t in valid_types)}]")
