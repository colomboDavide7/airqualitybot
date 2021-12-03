######################################################
#
# Author: Davide Colombo
# Date: 03/12/21 20:04
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import airquality.command.init.purpfact as purpfact
import airquality.command.initsrv.geofact as geofact


def get_init_factory_cls(sensor_type: str):
    function_name = get_init_factory_cls.__name__
    valid_types = ["purpleair", "geonames"]

    if sensor_type == 'purpleair':
        return purpfact.PurpleairInitFactory
    elif sensor_type == "geonames":
        return geofact.InitServiceCommandFactory
    else:
        raise SystemExit(f"{function_name}: bad type => VALID TYPES: [{'|'.join(t for t in valid_types)}]")
