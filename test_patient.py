import unittest
from patient import patient_make_booking, patient_cancels_booking, patient_view_booking, patient_view_open_booking


class PatientTest(unittest.TestCase):
    def test_patient_make_booking(self):
        check = patient_make_booking.booking()
        self.assertEqual(check, "You have just made an appointment.")

    def test_patient_cancels_booking(self):
        check = patient_cancels_booking.cancel_booking()
        self.assertEqual(check, "Booking cancelled.")

    def test_view_booking(self):
        check = patient_view_booking.view_booking()
        self.assertEqual(check, """These are your bookings:
        15h00 - Booking with BoJack for Toy Robot 4.""")

    def test_view_open_booking(self):
        check = patient_view_open_booking.view_open_bookings()
        self.assertEqual(check, """
    9:00 hangman 1 - Summer Smith
    9:30 recursion - Morty Smith
    10:00 TDD(unit testing) - Rick Sanchez
    """)


if __name__ == '__main__':
    unittest.main()
