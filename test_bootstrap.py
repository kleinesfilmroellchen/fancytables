import unittest
import stackprinter
import logging


def test_suite():
    logging.basicConfig(level=logging.DEBUG)
    stackprinter.set_excepthook(style="darkbg")
    test_loader = unittest.TestLoader()
    suite = test_loader.discover(start_dir="tests", top_level_dir=".")
    return suite
