import datetime
from django.db import models
from django.utils import timezone


class Question(models.Model):
    """
    Represents a poll question.
    """

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    end_date = models.DateTimeField('end date', null=True)

    def __str__(self):
        """
        Returns a string representation of the question, which is the question text.
        """
        return self.question_text

    def was_published_recently(self):
        """
        Checks if the question was published within the last day.
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


class Choice(models.Model):
    """
    Represents a choice in a poll, related to a specific question.
    """

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        """
        Returns a string representation of the choice, which is the choice text.
        """
        return self.choice_text
