######################################################
#
# Author: Davide Colombo
# Date: 03/01/22 20:52
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from dataclasses import dataclass


@dataclass
class ServiceParam(object):
    """
    A *dataclass* that defines the raw datastructure for the service's API parameters queried from the database.
    """

    api_key: str                    # The service's API key.
    n_requests: int                 # The number of requests done associated to the *api_key* above.

    def __repr__(self):
        return f"{type(self).__name__}(api_key=XXX, n_requests={self.n_requests})"
