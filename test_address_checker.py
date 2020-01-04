from address_checker import AddressChecker, SubdistrictPayload
import unittest


class TestAddressChecker(unittest.TestCase):

    def setUp(self):
        self.subdistrict = SubdistrictPayload.load_subdistricts('id')
        self.address_checker = AddressChecker(subdistricts=self.subdistrict, key_index='subdistrict_code')

    def test_get_sim_subdistrict(self):
        result = self.address_checker.get_sim_subdistrict('pameungpek')

        expected = [
            {
                "score": 1,
                "subdistrict_code": "32.04.14"
            },
            {
                "score": 1,
                "subdistrict_code": "32.05.27"
            }
        ]
        self.assertEqual(result, expected)

    def test_get_sim_subdistrict_include_only(self):
        include_only = ["32.04.14"]
        result = self.address_checker.get_sim_subdistrict('pameungpek', include_only)
        expected = [
            {
                "score": 1,
                "subdistrict_code": "32.04.14"
            }
        ]
        self.assertEqual(result, expected)

    def test_get_sim_city(self):
        result = self.address_checker.get_sim_city('kota cimhi', count=1)
        expected = [
            {
                "score": 1,
                "subdistrict_code": "32.77.01"
            }
        ]

        self.assertEqual(result, expected)

    def test_get_sim_city_include_only(self):
        include_only = ["32.77.01"]
        result = self.address_checker.get_sim_city('kota cimhi', include_only=include_only, count=2)
        expected = [
            {
                "score": 1,
                "subdistrict_code": "32.77.01"
            }
        ]

        self.assertEqual(result, expected)

    def test_suggest(self):
        result = self.address_checker.suggest('pameungpek', 'bandung')
        expected = [
            {'score': 5,
             'subdistrict_code': '32.04.14'}
        ]
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
