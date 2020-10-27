import unittest

from mock import Mock

from fawkes.constants import constants
from fawkes.review.review import Review
from fawkes.slackbot.slackbot import generate_star_from_rating, get_rating_color, get_sentiment_color, get_jira_details


class SlackbotTest(unittest.TestCase):

    def test_generate_star_from_rating(self):
        self.assertEqual("", generate_star_from_rating(-1))
        self.assertEqual("", generate_star_from_rating(0))
        self.assertEqual("*", generate_star_from_rating(1))
        self.assertEqual("*****", generate_star_from_rating(5))

    def test_get_rating_color(self):
        self.assertEqual("good", get_rating_color(4))
        self.assertEqual("good", get_rating_color(5))

        self.assertEqual("danger", get_rating_color(1))
        self.assertEqual("danger", get_rating_color(2))

        self.assertEqual("warning", get_rating_color(3))

    def test_get_sentiment_color(self):
        self.assertEqual("warning", get_sentiment_color(0))
        self.assertEqual("good", get_sentiment_color(50))
        self.assertEqual("danger", get_sentiment_color(-50))

    def test_get_jira_details(self):
        test_review = Review("Raw review for unit test",
                             message="Review message from slackbot test",
                             timestamp=100,
                             timestamp_format=constants.UNIX_TIMESTAMP)
        mock_app_config = Mock()
        mock_app_config.jira_config.bug_type = "bug_type"
        mock_app_config.jira_config.story_type = "story_type"
        mock_app_config.jira_config.project_id = 'some_project_id'
        mock_app_config.jira_config.base_url = "jira.com"
        actual_get_jira_details_bug = get_jira_details(test_review, mock_app_config, constants.BUG)

        self.assertEqual('jira.com/secure/CreateIssueDetails!init.jspa?summary=REVIEW+Feeback+on+%3A+uncategorized&description=Review+message+from+slackbot+test%0A%0A+Details+%3A+%0A+%7Bcode%3Ajson%7D%7B%0A++++%22message%22%3A+%22Review+message+from+slackbot+test%22%2C%0A++++%22timestamp%22%3A+%221969%2F12%2F31+16%3A01%3A40%22%2C%0A++++%22rating%22%3A+null%2C%0A++++%22user_id%22%3A+null%2C%0A++++%22app_name%22%3A+%22%22%2C%0A++++%22channel_name%22%3A+%22%22%2C%0A++++%22channel_type%22%3A+%22%22%2C%0A++++%22hash_id%22%3A+%22354f4fdfe7bdaff270f0ba144c4e1df90439eef1%22%2C%0A++++%22derived_insight%22%3A+%7B%0A++++++++%22sentiment%22%3A+null%2C%0A++++++++%22category%22%3A+%22uncategorized%22%2C%0A++++++++%22extra_properties%22%3A+%7B%7D%0A++++%7D%0A%7D%7Bcode%7D&issuetype=bug_type&pid=some_project_id&labels=Fawkes',
                         actual_get_jira_details_bug)

        actual_get_jira_details_feature = get_jira_details(test_review, mock_app_config, constants.FEATURE)
        self.assertEqual('jira.com/secure/CreateIssueDetails!init.jspa?summary=REVIEW+Feeback+on+%3A+uncategorized&description=Review+message+from+slackbot+test%0A%0A+Details+%3A+%0A+%7Bcode%3Ajson%7D%7B%0A++++%22message%22%3A+%22Review+message+from+slackbot+test%22%2C%0A++++%22timestamp%22%3A+%221969%2F12%2F31+16%3A01%3A40%22%2C%0A++++%22rating%22%3A+null%2C%0A++++%22user_id%22%3A+null%2C%0A++++%22app_name%22%3A+%22%22%2C%0A++++%22channel_name%22%3A+%22%22%2C%0A++++%22channel_type%22%3A+%22%22%2C%0A++++%22hash_id%22%3A+%22354f4fdfe7bdaff270f0ba144c4e1df90439eef1%22%2C%0A++++%22derived_insight%22%3A+%7B%0A++++++++%22sentiment%22%3A+null%2C%0A++++++++%22category%22%3A+%22uncategorized%22%2C%0A++++++++%22extra_properties%22%3A+%7B%7D%0A++++%7D%0A%7D%7Bcode%7D&issuetype=story_type&pid=some_project_id&labels=Fawkes',
                         actual_get_jira_details_feature)
