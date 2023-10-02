import unittest
from datetime import datetime, timedelta
import pytz
from main import format_last_seen, get_user_data
from unittest.mock import patch

# Define a class for your unit tests
class TestUserData(unittest.TestCase):
    def setUp(self):

        self.current_time = datetime.now(pytz.UTC)

    def test_format_last_seen_just_now(self):
        last_seen = self.current_time - timedelta(seconds=15)
        lang = "en"
        expected_result = "just now"
        self.assertEqual(format_last_seen(last_seen, lang), expected_result)

    def test_format_last_seen_less_than_a_minute_ago(self):
        last_seen = self.current_time - timedelta(seconds=45)
        lang = "en"
        expected_result = "less than a minute ago"
        self.assertEqual(format_last_seen(last_seen, lang), expected_result)

    def test_format_last_seen_a_couple_of_minutes_ago(self):
        last_seen = self.current_time - timedelta(minutes=45)
        lang = "en"
        expected_result = "a couple of minutes ago"
        self.assertEqual(format_last_seen(last_seen, lang), expected_result)

    def test_format_last_seen_an_hour_ago(self):
        last_seen = self.current_time - timedelta(minutes=90)
        lang = "en"
        expected_result = "an hour ago"
        self.assertEqual(format_last_seen(last_seen, lang), expected_result)

    def test_format_last_seen_today(self):
        last_seen = self.current_time - timedelta(hours=20)
        lang = "en"
        expected_result = "today"
        self.assertEqual(format_last_seen(last_seen, lang), expected_result)

    def test_format_last_seen_yesterday(self):
        last_seen = self.current_time - timedelta(hours=40)
        lang = "en"
        expected_result = "yesterday"
        self.assertEqual(format_last_seen(last_seen, lang), expected_result)

    def test_format_last_seen_this_week(self):
        last_seen = self.current_time - timedelta(days=5)
        lang = "en"
        expected_result = "this week"
        self.assertEqual(format_last_seen(last_seen, lang), expected_result)

    def test_format_last_seen_a_long_time_ago(self):
        last_seen = self.current_time - timedelta(days=123)
        lang = "en"
        expected_result = "a long time ago"
        self.assertEqual(format_last_seen(last_seen, lang), expected_result)

class TestGetUserData(unittest.TestCase):
    @patch('main.fetch_user_data')
    def test_get_user_data_single_page(self, mock_fetch_user_data):
        mock_response = {'data': [{'nickname': 'first_user', 'lastSeenDate': '2023-10-01T12:00:00Z'}]}
        mock_fetch_user_data.side_effect = [mock_response, []]

        user_data = get_user_data()

        self.assertEqual(len(user_data), 1)
        self.assertEqual(user_data[0]['nickname'], 'first_user')

    @patch('main.fetch_user_data')
    def test_get_user_data_multiple_pages(self, mock_fetch_user_data):
        mock_response1 = {'data': [{'nickname': 'first_user', 'lastSeenDate': '2023-10-01T12:00:00Z'}]}
        mock_response2 = {'data': [{'nickname': 'second_user', 'lastSeenDate': '2023-10-01T13:00:00Z'}]}
        mock_response3 = {}
        mock_fetch_user_data.side_effect = [mock_response1, mock_response2, mock_response3]

        user_data = get_user_data()

        self.assertEqual(len(user_data), 2)
        self.assertEqual(user_data[0]['nickname'], 'first_user')
        self.assertEqual(user_data[1]['nickname'], 'second_user')


if __name__ == "__main__":
    unittest.main()
