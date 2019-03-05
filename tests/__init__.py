import unittest
import os
from tests.tests_user import *


def suit():
    suite = unittest.TestSuite()
    suite.addTest(WidgetTestCase('test_default_widget_size'))
    suite.addTest(WidgetTestCase('test_widget_resize'))
    return suite


if __name__ == "tests":
    # files = os.listdir("tests/user")
    # print(files)
    # run_tests()
    pass
