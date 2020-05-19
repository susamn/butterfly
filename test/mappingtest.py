import unittest
from engine import transform


class MappingTest(unittest.TestCase):
    def test_simple_mapping(self):
        result = transform("testdata/weather.json", "testdata/weather-mapping.json")
        print(result)
