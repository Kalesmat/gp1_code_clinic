import unittest
import sys


class MyTestCase(unittest.TestCase):

    def test_clinic_succeeds(self):
        import test_clinic
        test_result = run_unittests("test_clinic")
        self.assertTrue(test_result.wasSuccessful(), "unit tests should succeed")

    def test_clinician_create_succeeds(self):
        import test_clinician_create
        test_result = run_unittests("test_clinician_create")
        self.assertTrue(test_result.wasSuccessful(), "unit tests should succeed")

    def test_clinician_delete_succeeds(self):
        import test_clinician_delete
        test_result = run_unittests("test_clinician_delete")
        self.assertTrue(test_result.wasSuccessful(), "unit tests should succeed")

    def test_patient_succeeds(self):
        import test_patient
        test_result = run_unittests("test_patient")
        self.assertTrue(test_result.wasSuccessful(), "unit tests should succeed")

    def test_view_succeeds(self):
        import test_view
        test_result = run_unittests("test_view")
        self.assertTrue(test_result.wasSuccessful(), "unit tests should succeed")

    def test_view_booked_succeeds(self):
        import test_review
        test_result = run_unittests("test_view_booked")
        self.assertTrue(test_result.wasSuccessful(), "unit tests should succeed")

    def test_view_available_succeeds(self):
        import test_review
        test_result = run_unittests("test_view_available")
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