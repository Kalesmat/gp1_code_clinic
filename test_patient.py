import unittest
from unittest.mock import patch
from io import StringIO
import sys
import code_clinic
from clinician import create
import datetime
from patient import patient_make_booking, patient_cancels_booking, patient_view_booking, patient_view_open_booking


class PatientTest(unittest.TestCase):
    def test_patient_make_booking(self):
        # for booking

        summary = 'Testing for unittests.'
        description = 'Test booking and cancelling with the unittest as summary'
        start_d = datetime.datetime.now().date() + datetime.timedelta(hours=24)
        start_t = '10:00'
        end_t = '10:30'

        # functions that help with testing for booking and cancellations

        service = code_clinic.startup()
        creator, admin = "Fake Creator", "fake.creator@gmail.com"
        create_slot = create.do_create(service, summary, description, start_d, start_t, end_t, creator, admin)
        test_id = create_slot['id']
        my_events = patient_view_booking.view_booking(service, admin)

        with patch('sys.stdin', StringIO(f'{test_id}\n')):
            the_stdout = sys.stdout
            new_string = StringIO()
            sys.stdout = new_string
            username, email = "Booker", "fake.booking@gmail.com"
            book = patient_make_booking.booking(service, username, email)
            test_result = f"{summary} is successfully booked.."
            self.assertTrue(book, test_result)
            self.assertTrue(test_id, my_events is True)
            sys.stdout = the_stdout

    def test_patient_make_double_booking(self):
        # for booking

        summary = 'Testing for unittests.'
        description = 'Test booking and cancelling with the unittest as summary'
        start_d = datetime.datetime.now().date() + datetime.timedelta(hours=24)
        start_t = '10:00'
        end_t = '10:30'

        # functions that help with testing for booking and cancellations

        service = code_clinic.startup()
        creator, admin = "Fake Creator", "fake.creator@gmail.com"
        create_slot = create.do_create(service, summary, description, start_d, start_t, end_t, creator, admin)
        test_id = create_slot['id']

        with patch('sys.stdin', StringIO(f'{test_id}\n')):
            the_stdout = sys.stdout
            new_string = StringIO()
            sys.stdout = new_string
            username, email = "Booker", "fake.booking@gmail.com"
            book = patient_make_booking.booking(service, username, email)
            test_result = f"{username}, number of attendees has been reached, please check for the next slot."
            self.assertTrue(book, test_result)
            sys.stdout = the_stdout

    def test_patient_make_booking_if_is_volunteer(self):
        # for booking

        summary = 'Testing for unittests.'
        description = 'Test booking and cancelling with the unittest as summary'
        start_d = datetime.datetime.now().date() + datetime.timedelta(hours=24)
        start_t = '10:00'
        end_t = '10:30'

        # functions that help with testing for booking and cancellations

        service = code_clinic.startup()
        creator, admin = "Fake Creator", "fake.creator@gmail.com"
        create_slot = create.do_create(service, summary, description, start_d, start_t, end_t, creator, admin)
        test_id = create_slot['id']

        with patch('sys.stdin', StringIO(f'{test_id}\n')):
            the_stdout = sys.stdout
            new_string = StringIO()
            sys.stdout = new_string
            username, email = "Fake Creator", "fake.creator@gmail.com"
            book = patient_make_booking.booking(service, username, email)
            test_result = f'{username}, Unfortunately you cannot book your own event..'
            self.assertTrue(book, test_result)
            sys.stdout = the_stdout

    def test_patient_make_booking_invalid_eventid(self):
        service = code_clinic.startup()
        username, email = "Booker", "fake.booking@gmail.com"

        with patch('sys.stdin', StringIO('y0hI@mFak3eee33\n')):
            the_stdout = sys.stdout
            new_string = StringIO()
            sys.stdout = new_string
            book = patient_make_booking.booking(service, username, email)
            test_result = "Unfortunately that is an invalid event ID.."
            self.assertFalse(book, test_result)
            sys.stdout = the_stdout

    def test_patient_make_booking_invalid_empty(self):
        service = code_clinic.startup()
        username, email = "Booker", "fake.booking@gmail.com"

        with patch('sys.stdin', StringIO(f'{None}\n')):
            the_stdout = sys.stdout
            new_string = StringIO()
            sys.stdout = new_string
            book = patient_make_booking.booking(service, username, email)
            test_result = "Unfortunately that is an invalid event ID.."
            self.assertFalse(book, test_result)
            sys.stdout = the_stdout

    def test_patient_cancels_booking(self):
        summary = 'Testing for unittests.'
        description = 'Test booking and cancelling with the unittest as summary'
        start_d = datetime.datetime.now().date() + datetime.timedelta(hours=24)
        start_t = '10:00'
        end_t = '10:30'

        # functions that help with testing for booking and cancellations

        service = code_clinic.startup()
        creator, admin = "Fake Creator", "fake.creator@gmail.com"
        create_slot = create.do_create(service, summary, description, start_d, start_t, end_t, creator, admin)
        test_id = create_slot['id']
        my_events = patient_view_booking.view_booking(service, admin)

        username, email = "Booker", "fake.booking@gmail.com"
        my_events = patient_view_booking.view_booking(service, email)

        with patch('sys.stdin', StringIO(f'{test_id}\n')):
            the_stdout = sys.stdout
            new_string = StringIO()
            sys.stdout = new_string
            cancel = patient_cancels_booking.cancel_booking(service, username, email)
            test_result = f"{username}, You have successfully cancelled slot."
            self.assertTrue(cancel, test_result)
            self.assertTrue(test_id, my_events is True)
            sys.stdout = the_stdout

    def test_patient_cancels_booking_my_events_is_none(self):
        service = code_clinic.startup()
        username, email = "Booker", "fake.booking@gmail.com"
        my_events = patient_view_booking.view_booking(service, email)

        with patch('sys.stdin', StringIO(f'{my_events}\n')):
            the_stdout = sys.stdout
            new_string = StringIO()
            sys.stdout = new_string
            cancel = patient_cancels_booking.cancel_booking(service, username, email)
            self.assertFalse(cancel, my_events is False)
            sys.stdout = the_stdout

    def test_patient_cancels_booking_if_event_is_other_patients(self):
        service = code_clinic.startup()
        username, email = "Booker", "fake.booking@gmail.com"
        events = patient_view_open_booking.view_open_bookings(service)

        with patch('sys.stdin', StringIO(f'{events}\n')):
            the_stdout = sys.stdout
            new_string = StringIO()
            sys.stdout = new_string
            cancel = patient_cancels_booking.cancel_booking(service, username, email)
            test_result = f"{username}, You are not the attendee on this event."
            self.assertFalse(cancel, test_result)
            self.assertFalse(events is False)
            sys.stdout = the_stdout

    def test_patient_cancels_booking_invalid_eventid(self):
        service = code_clinic.startup()
        username, email = "Booker", "fake.booking@gmail.com"

        with patch('sys.stdin', StringIO('y0hI@mFak3eee33\n')):
            the_stdout = sys.stdout
            new_string = StringIO()
            sys.stdout = new_string
            cancel = patient_cancels_booking.cancel_booking(service, username, email)
            test_result = "Unfortunately that is an invalid event ID.."
            self.assertFalse(cancel, test_result)
            sys.stdout = the_stdout

    def test_patient_cancels_booking_invalid_empty(self):
        service = code_clinic.startup()
        username, email = "Booker", "fake.booking@gmail.com"

        with patch('sys.stdin', StringIO(f'{None}\n')):
            the_stdout = sys.stdout
            new_string = StringIO()
            sys.stdout = new_string
            cancel = patient_cancels_booking.cancel_booking(service, username, email)
            test_result = "Unfortunately that is an invalid event ID.."
            self.assertFalse(cancel, test_result)
            sys.stdout = the_stdout

    def test_view_booking(self):
        # check = patient_view_booking.view_booking()
        # self.assertEqual(check, """These are your bookings:
        # 15h00 - Booking with BoJack for Toy Robot 4.""")
        pass

    def test_view_open_booking(self):
        #     check = patient_view_open_booking.view_open_bookings()
        #     self.assertEqual(check, """
        # 9:00 hangman 1 - Summer Smith
        # 9:30 recursion - Morty Smith
        # 10:00 TDD(unit testing) - Rick Sanchez
        # """)
        pass


if __name__ == '__main__':
    unittest.main()
