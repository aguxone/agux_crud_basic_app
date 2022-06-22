from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse


# def index(request):
#     return HttpResponse("Hello, world.a30499ad You're at the polls index.")

#Django tutorial 3 we replace the index
# The index will output the latest question it seems
from django.template import loader
from .models import Question
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    # return HttpResponse(template.render(context, request))
    # We can use that full return with http response, or the following
    #shortcut. This shortcut doesn't need to import he loader nor
    # httpresponse! (but of course imports render)
    return render(request, 'polls/index.html', context)

# Leave the rest of the views (detail, results, vote) unchanged


#Django tutorial part 3, we add some new views to polls
# a detail, results and vote page

# We can use a detail that returns the parameter after the slash
# def detail(request, question_id):
#     return HttpResponse("You're looking at question %s." % question_id)

#But we'll use another one that returns the parameter alone
# or raises an error if nothing is inputed
from django.shortcuts import get_object_or_404

def detail(request, question_id):

    # We could use the classic "try" of python
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404

    #Or use a django function shortcut which includes everything
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)

# Code to autograde the assignment 3#
def owner(request):
    return HttpResponse("Hello, world. fc37e65a is the polls index. Django3_w1_A1_code= 6c9084f3")

# Django tutorial 4 code, Vote view #
#########################
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

## NOW the vote results part
from django.shortcuts import get_object_or_404, render

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

# Django tutorial 4, GENERIC VIEWS, the ones we are using
# right now; note hey use classes and are very short.
# The vote one will not be modified, as there is no generic view
# for that one.

# Note that for template_name it uses polls/detail.html as an example
#, although it is located in polls/templates/polls/detail.html.
# It just understands this convention.

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Choice, Question

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'