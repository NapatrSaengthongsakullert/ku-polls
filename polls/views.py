from django.db.models import F
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from .models import Choice, Question


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
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]


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

    def get(self, request, *args, **kwargs):
        """To back to index page if not found"""
        try:
            question = get_object_or_404(Question, pk=kwargs['pk'])
        except Http404:
            messages.error(
                request, "Question is not available")
        if not question.can_vote():
            messages.error(request, "Question is not available")
            return HttpResponseRedirect(reverse('polls:index'))
        return super().get(request, *args, **kwargs)


class ResultsView(generic.DetailView):
    """
    View to display the results of a specific question, including the
    number of votes each choice has received.
    """
    model = Question
    template_name = "polls/results.html"


def vote(request, question_id):
    """
    Handles the voting process for a specific question.
    """
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
