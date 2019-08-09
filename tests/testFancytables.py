import unittest

from fancytables import FancyTable


class FancyTableTest(unittest.TestCase):

    def setUp(self):
        self.ft = FancyTable(headers=["a", "b", "c"])

    def test_basic(self):
        # all of these must not throw
        table = FancyTable(headers=["a", "b", "c"])
        del table
        table = FancyTable("a", "b", "c")

        table = FancyTable()
        self.assertEqual(table.headers, [], "Empty headers")
        self.assertEqual(table.data, [], 'Empty data if argument not given')

    def test_headers(self):
        self.assertEqual(self.ft.headers, [
            {'title': 'a', 'important': False},
            {'title': 'b', 'important': False},
            {'title': 'c', 'important': False}], "Header shorthand")

        table = FancyTable(
            {'title': 'a', 'important': False},
            {'title': 'b', 'important': True},
            {'title': 'd', 'important': False})
        self.assertEqual(table.headers, [
            {'title': 'a', 'important': False},
            {'title': 'b', 'important': True},
            {'title': 'd', 'important': False}], "Header full constructor")

    def test_dataadding(self):
        # basic adding
        table = FancyTable("a", "b", "c")
        table += ["string", ["nothing", 223], False]
        self.assertEqual(len(table.data), 1, 'Length operation on table data')

        # subtracting
        self.assertRaises(ValueError, lambda x: table - (-10),
                          'Subtract negative rows')

        self.assertRaises(TypeError, lambda: table - "str",
                          'Subtracting with non-int')

        table -= 1
        self.assertEqual(len(table.data), 0, "Subtracting rows")

        # adding w/ copy
        table += ["string", [], False]
        othertable = table + ["a", [23, 5], True]
        self.assertEqual(
            table.data, [["string", [], False]], 'Copy is created at simple addition')
        self.assertEqual(len(othertable.data), 2, 'Copied table was modified')

    def test_format(self):
        pass
