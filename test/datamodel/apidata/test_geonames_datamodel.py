# ======================================
# @author:  Davide Colombo
# @date:    2022-01-20, gio, 20:02
# ======================================
from unittest import TestCase, main
from airquality.datamodel.fromfile import GeonamesDM


class TestGeonamesDatamodel(TestCase):

    def test_geonames_place_datamodel(self):
        line = [
            "IT",
            "27100",
            "Pavia'",
            "Lombardia'",
            "statecode",
            "Pavia'",
            "PV",
            "community",
            "communitycode",
            "45",
            "9",
            "4"
        ]
        data = GeonamesDM(*line)
        self.assertEqual(data.postal_code, "27100")
        self.assertEqual(data.place_name, "Pavia")
        self.assertEqual(data.country_code, "IT")
        self.assertEqual(data.state, "Lombardia")
        self.assertEqual(data.province, "Pavia")
        self.assertEqual(data.latitude, 45)
        self.assertEqual(data.longitude, 9)


if __name__ == '__main__':
    main()
