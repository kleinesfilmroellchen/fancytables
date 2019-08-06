import unittest
from fancytables import FancyTable


class FancyTableTest(unittest.TestCase):

    def setUp(self):
        self.ft = FancyTable(["a", "b", "c"])

    def test_basic(self):
        # must not throw
        table = FancyTable(["a", "b", "c"])
        # ''
        del table
        table = FancyTable()
        self.assertEqual(table.headers, [], "Empty headers")
        self.assertEqual(table.data, [], 'Empty data if argument not given')

    def test_headers(self):
        self.assertEqual(self.ft.headers, [
            {'title': 'a', 'content': 'generic', 'important': False},
            {'title': 'b', 'content': 'generic', 'important': False},
            {'title': 'c', 'content': 'generic', 'important': False}], "Header shorthand")
        table = FancyTable([
            {'title': 'a', 'content': 'str', 'important': False},
            {'title': 'b', 'content': 'list', 'important': True},
            {'title': 'd', 'content': 'bool', 'important': False}])
        self.assertEqual(table.headers, [
            {'title': 'a', 'content': 'str', 'important': False},
            {'title': 'b', 'content': 'list', 'important': True},
            {'title': 'd', 'content': 'bool', 'important': False}], "Header full constructor")

        def validation_func(x):
            if x[0] != 'a':
                raise ValueError
            return x
        table = FancyTable([
            {'title': 'a', 'content': 'generic', 'important': False},
            {'title': 'b', 'content': validation_func, 'important': False}])
        table += ["x", 'abc']
        self.assertRaises(TypeError, lambda: table +
                          ["y", "zz"], 'Custom validation function')

    def test_dataadding(self):
        table = FancyTable([
            {'title': 'a', 'content': 'str', 'important': False},
            {'title': 'b', 'content': 'list', 'important': True},
            {'title': 'd', 'content': 'bool', 'important': False}])
        self.assertRaises(TypeError,
                          lambda: table + ["a", "b", "c"],
                          'Incorrect type')

        table = FancyTable([
            {'title': 'a', 'content': 'str', 'important': False},
            {'title': 'b', 'content': 'list', 'important': True},
            {'title': 'd', 'content': 'bool', 'important': False}])
        table += [["a", [], True],  # match types
                  ["a", "b", "c"]]
        self.assertEqual(table.data, [["a", [], True]],
                         'Incorrect insertion skipped')
        del table.data
        table += ["string", ["nothing", 223], False]
        self.assertEqual(table.data, [["string", ["nothing", 223], False]],
                         'Simple correct insertion, one nesting')
        self.assertEqual(len(table.data), 1, 'Length operation on table data')

        table -= 1
        self.assertEqual(len(table.data), 0, "Subtracting rows")

        table += ["string", [], False]
        othertable = table + ["a", [23, 5], True]
        self.assertEqual(
            table.data, [["string", [], False]], 'Copy is created at simple addition')
        self.assertEqual(len(othertable.data), 2, 'Copied table was modified')

        self.assertRaises(TypeError, lambda: table - "str",
                          'Subtracting with non-int')

    def test_format(self):
        pass
