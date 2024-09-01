import datetime
from django.test import TestCase
from django.utils import timezone
from .models import Question
from django.urls import reverse


class QuestionModelTests(TestCase):
    """
    Test cases for the Question model, particularly the was_published_recently()
    method, which determines if a question was published within the last day.
    """

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_was_published_recently_with_exact_time(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is exactly the current time.
        """
        time = timezone.now()
        exact_time_question = Question(pub_date=time)
        self.assertIs(exact_time_question.was_published_recently(), True)

    def test_was_published_recently_with_within_one_day_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last 24 hours.
        """
        time = timezone.now() - datetime.timedelta(hours=12)
        within_one_day_question = Question(pub_date=time)
        self.assertIs(within_one_day_question.was_published_recently(), True)

    def test_is_published_with_future_pub_date(self):
        """is_published() returns False for questions whose pub_date is in the future."""
        future_date = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=future_date)
        self.assertFalse(future_question.is_published())

    def test_is_published_with_current_pub_date(self):
        """is_published() returns True for questions whose pub_date is now."""
        current_date = timezone.now()
        current_question = Question(pub_date=current_date)
        self.assertTrue(current_question.is_published())

    def test_is_published_with_past_pub_date(self):
        """is_published() returns True for questions whose pub_date is in the past."""
        past_date = timezone.now() - datetime.timedelta(days=30)
        past_question = Question(pub_date=past_date)
        self.assertTrue(past_question.is_published())

    def test_cannot_vote_after_end_date(self):
        """can_vote() returns False if the end_date is in the past."""
        past_end_date = timezone.now() - datetime.timedelta(days=1)
        question = Question(pub_date=timezone.now() - datetime.timedelta(days=2), end_date=past_end_date)
        self.assertFalse(question.can_vote())

    def test_can_vote_before_end_date(self):
        """can_vote() returns True if the end_date is in the future."""
        future_end_date = timezone.now() + datetime.timedelta(days=1)
        question = Question(pub_date=timezone.now() - datetime.timedelta(days=2), end_date=future_end_date)
        self.assertTrue(question.can_vote())

    def test_can_vote_without_end_date(self):
        """can_vote() returns True if there is no end_date and the question is published."""
        question = Question(pub_date=timezone.now() - datetime.timedelta(days=2), end_date=None)
        self.assertTrue(question.can_vote())

def create_question(question_text, days):
    """
    Create a question with the given `question_text` and publish it the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionIndexViewTests(TestCase):
    """
    Test cases for the index view of the polls app, which displays a list
    of the latest questions.
    """

    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question2, question1],
        )


class QuestionDetailViewTests(TestCase):
    """
    Test cases for the detail view of the polls app, which displays the
    details of a specific question.
    """

    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text="Future question.", days=5)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text="Past Question.", days=-5)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
