from unittest import TestCase

from operations import load_csv


class CSVTest(TestCase):
    def test_can_read_dict(self):
        csv = """
Hello,World
1,2        
"""
        result = load_csv(csv)

        print(result)
