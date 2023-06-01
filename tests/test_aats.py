import datetime
import unittest
from unittest.mock import MagicMock, patch

from aats import update_attendance


class TestUpdateAttendance(unittest.TestCase):
    def setUp(self):
        # Set up mock objects
        self.sheet = MagicMock()
        self.worksheet = MagicMock()
        self.form = MagicMock()
        self.response1 = MagicMock()
        self.response2 = MagicMock()

        # Set up response data for mock objects
        self.response1.values.return_value = [
            '03/01/2022 09:00:00 AM',
            'John Doe',
            'Present'
        ]
        self.response2.values.return_value = [
            '03/01/2022 09:15:00 AM',
            'Jane Smith',
            'Late'
        ]
        self.responses = [self.response1, self.response2]

    @patch('attendance_tracker.client')
    @patch('attendance_tracker.send_email')
    def test_update_attendance(self, mock_send_email, mock_client):
        # Set up mock objects
        mock_client.open.return_value = self.sheet
        self.sheet.worksheet.return_value = self.worksheet
        self.form.get_form_responses.return_value = self.responses

        # Call the function
        update_attendance('Test Sheet', 'Test Worksheet',
                          'https://forms.google.com/test-form', 'test@example.com')

        # Assert that the mock objects were called with the correct arguments
        mock_client.open.assert_called_once_with('Test Sheet')
        self.sheet.worksheet.assert_called_once_with('Test Worksheet')
        self.form.get_form_responses.assert_called_once()
        self.worksheet.insert_row.assert_any_call([
            '03/01/2022',
            '09:00:00 AM',
            'John Doe',
            'Present'
        ], 1)
        self.worksheet.insert_row.assert_any_call([
            '03/01/2022',
            '09:15:00 AM',
            'Jane Smith',
            'Late'
        ], 2)
        mock_send_email.assert_called_once_with('test@example.com', 'John Doe is Present on 03/01/2022',
                                                'John Doe is Present on 03/01/2022 09:00:00 AM.\nJane Smith is Late on 03/01/2022 09:15:00 AM.')


if __name__ == '__main__':
    unittest.main()
