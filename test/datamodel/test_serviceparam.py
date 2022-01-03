######################################################
#
# Author: Davide Colombo
# Date: 03/01/22 20:50
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from unittest import TestCase, main
from airquality.datamodel.service_param import ServiceParam


class TestServiceParam(TestCase):

    def test_service_param(self):
        param = ServiceParam(
            api_key="some_key", n_requests=0
        )
        self.assertEqual(param.api_key, "some_key")
        self.assertEqual(param.n_requests, 0)
        self.assertEqual(repr(param), "ServiceParam(api_key=XXX, n_requests=0)")


if __name__ == '__main__':
    main()
