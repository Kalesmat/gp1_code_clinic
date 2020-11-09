import unittest
import sys


class MyTestCase(unittest.TestCase):

    def test_unittest_exist(self):
        import test_clinic
        self.assertTrue('test_clinic' in sys.modules, "test_clinic module should be found")

    def test_unittest_succeeds(self):
        import test_clinic
        test_result = run_unittests("test_clinic")
        self.assertTrue(test_result.wasSuccessful(), "unit tests should succeed")


def run_unittests(test_file):
    """
    Use this method to discover unittests at specified path, and run them
    :param test_file: Name of unittest file
    :return: TestResult
    """
    import unittest
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromName(test_file)

    runner = unittest.TextTestRunner()
    return runner.run(suite)


if __name__ == '__main__':
    unittest.main()