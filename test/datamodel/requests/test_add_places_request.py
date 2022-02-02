# ======================================
# @author:  Davide Colombo
# @date:    2022-01-20, gio, 21:01
# ======================================
from unittest import TestCase, main
from airquality.datamodel.geometry import PostgisPoint
from airquality.datamodel.requests import AddPlaceRequest


def _place_location_test_data():
    wgs84_srid = 4326
    return PostgisPoint(latitude=45, longitude=9, srid=wgs84_srid)


def _expected_geom_from_text_location():
    return "ST_GeomFromText('POINT(9 45)', 4326)"


class TestAddPlacesRequest(TestCase):

# =========== TEST METHODS
    def test_request_model_for_adding_geonames_country_data(self):
        request = AddPlaceRequest(
            placename="fakename",
            poscode="fakecode",
            state="fakestate",
            geolocation=_place_location_test_data(),
            countrycode="fakecode",
            province="fake_province"
        )
        self.assertEqual(request.placename, "fakename")
        self.assertEqual(request.poscode, "fakecode")
        self.assertEqual(request.state, "fakestate")
        self.assertEqual(request.countrycode, "fakecode")
        self.assertEqual(request.province, "fake_province")
        self.assertEqual(
            str(request.geolocation),
            _expected_geom_from_text_location()
        )


if __name__ == '__main__':
    main()
