import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

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

    def is_published(self):
        """Returns True if current date is on or after question’s publication date."""
        now = timezone.now()
        return now >= self.pub_date

    def can_vote(self):
        """Returns True if voting is allowed for this question."""
        if self.end_date:
            return self.is_published and timezone.now() <= self.end_date
        return self.is_published()


class Choice(models.Model):
    """
    Represents a choice in a poll, related to a specific question.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        """
        Returns a string representati6n of the choice, which is the choice text.
        """
        return self.choice_text

    @property
    def votes(self) -> int:
        """Return votes amount of that choice."""
        return Vote.objects.filter(choice=self).count()


class Vote(models.Model):
    """This model is used to collected votes for a choice with username."""
    user = models.ForeignKey(
        User, blank=False, null=False, on_delete=models.CASCADE)
    choice = models.ForeignKey(
        Choice, blank=False, null=False, on_delete=models.CASCADE)

    @property
    def question(self):
        """Question of the choice."""
        return self.choice.question