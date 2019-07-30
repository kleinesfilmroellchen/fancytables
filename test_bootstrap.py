import unittest


def test_suite():
    test_loader = unittest.TestLoader()
    suite = test_loader.discover(start_dir="tests", top_level_dir=".")
    return suite
