"""IMPORT."""
import logging
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from .models import Choice, Question, Vote
from django.contrib.auth.decorators import login_required

logger = logging.getLogger('polls')


class IndexView(generic.ListView):
    """
    View to display a list of the latest five published questions.

    Only questions with a publication date that is not in the future
    are included in the list. The questions are ordered by publication
    date in descending order.
    """

    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")


class DetailView(generic.DetailView):
    """
    View to display the details of a specific question.

    The view excludes any questions that are not yet published (i.e., those with a
    publication date in the future).
    """

    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

    def get(self, request, pk):
        """
        Redirect to index page if questionID is not found.
        """
        try:
            self.question = Question.objects.get(pk=pk)
        except Question.DoesNotExist:
            return redirect("polls:index")

        self.question = get_object_or_404(Question, pk=pk)
        try:
            vote = Vote.objects.get(user=request.user, choice__in=self.question.choice_set.all())
            previous_choice = vote.choice.choice_text
        except (Vote.DoesNotExist, TypeError):
            previous_choice = ""

        if self.question.can_vote():
            return render(request, self.template_name, {
                "question": self.question,
                "previous_vote": previous_choice
            })
        else:
            messages.error(request, f"Poll number {self.question.id} is not available to vote.")
            return redirect("polls:index")


class ResultsView(generic.DetailView):
    """
    View to display the results of a specific question, including the
    number of votes each choice has received.
    """

    model = Question
    template_name = "polls/results.html"

    def get(self, request, *args, **kwargs):
        """
        Redirect to index page if questionID is not found.
        """
        try:
            self.object = self.get_object()
            return super().get(request, *args, **kwargs)
        except Question.DoesNotExist:
            return redirect(reverse('polls:index'))


@login_required
def vote(request, question_id):
    """
    Process of voting.
    """
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        messages.error(request, "You didn't select a choice.")
        return redirect(reverse('polls:detail', args=(question.id,)))
    else:
        try:
            vote = Vote.objects.get(user=request.user, choice__question=question)
            previous_choice = vote.choice  # Save previous choice for comparison
            vote.choice = selected_choice
            vote.save()
            if previous_choice != selected_choice:
                messages.success(request, f'You changed your answer to "{selected_choice.choice_text}".')
            else:
                messages.success(request, f'Your vote for "{selected_choice.choice_text}" has been recorded.')
        except Vote.DoesNotExist:
            Vote.objects.create(user=request.user, choice=selected_choice)
            logger.info(f"User {request.user.username} voted on question {question.id} with choice {selected_choice.id}")
            messages.success(request, f'Your vote for "{selected_choice.choice_text}" has been recorded.')

        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
