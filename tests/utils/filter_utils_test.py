import time
import unittest
from datetime import datetime
from pytz import timezone

from fawkes.constants import constants
from fawkes.review.review import Review
from fawkes.utils.filter_utils import filter_reviews_by_channel, filter_reviews_by_time


class FilterUtilsTest(unittest.TestCase):

    def setUp(self):
        self.unix_time = time.time()
        self.timestamp = datetime.fromtimestamp(self.unix_time).replace(tzinfo=timezone("UTC"))
        self.test_reviews = [
            Review("Raw review for unit test 1",
                   message="Review message 1",
                   timestamp=self.unix_time + 10,
                   timestamp_format=constants.UNIX_TIMESTAMP,
                   review_timezone="UTC",
                   channel_name="channel_1"),
            Review("Raw review for unit test 2",
                   message="Review message 2",
                   timestamp=self.unix_time - 10,
                   timestamp_format=constants.UNIX_TIMESTAMP,
                   review_timezone="UTC",
                   channel_name="channel_2"),
            Review("Raw review for unit test 3",
                   message="Review message 3",
                   timestamp=self.unix_time + 5,
                   timestamp_format=constants.UNIX_TIMESTAMP,
                   review_timezone="UTC",
                   channel_name="channel_3"),
            Review("Raw review for unit test 4",
                   message="Review message 4",
                   timestamp=self.unix_time - 5,
                   timestamp_format=constants.UNIX_TIMESTAMP,
                   review_timezone="UTC",
                   channel_name="channel_4")
        ]

    def test_filter_reviews_by_channel(self):
        channel_filtered_reviews = filter_reviews_by_channel(self.test_reviews, set(["channel_2", "channel_4"]))
        self.assertEqual([self.test_reviews[1], self.test_reviews[3]], channel_filtered_reviews)

    def test_filter_reviews_by_time(self):
        time_filtered_reviews = filter_reviews_by_time(self.test_reviews, self.timestamp)
        self.assertEqual([self.test_reviews[0], self.test_reviews[2]], time_filtered_reviews)
