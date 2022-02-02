# ======================================
# @author:  Davide Colombo
# @date:    2022-01-20, gio, 19:57
# ======================================
from unittest import TestCase, main
from airquality.datamodel.fromapi import AtmotubeDM


class TestAtmotubeDatamodel(TestCase):

    def test_atmotube_datamodel(self):
        data = AtmotubeDM(
            time="2021-08-10T23:59:00.000Z",
            voc=0.17,
            pm1=8,
            pm25=10,
            pm10=11,
            t=29,
            h=42,
            p=1004.68,
            coords={'lat': 45.765, 'lon': 9.897}
        )

        self.assertEqual(data.time, "2021-08-10T23:59:00.000Z")
        self.assertEqual(data.voc, 0.17)
        self.assertEqual(data.pm1, 8)
        self.assertEqual(data.pm25, 10)
        self.assertEqual(data.pm10, 11)
        self.assertEqual(data.t, 29)
        self.assertEqual(data.h, 42)
        self.assertEqual(data.p, 1004.68)
        self.assertEqual(data.coords, {'lat': 45.765, 'lon': 9.897})


if __name__ == '__main__':
    main()
