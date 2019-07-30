import unittest
from fancytables import FancyTable


class FancyTableTest(unittest.TestCase):
    def test_basic(self):
        try:
            self.assertEqual(3, 3)
        except Exception as e:
            self.fail(str(e))

    def test_format(self):
        pass

    def test_parsing(self):
        pass
