from django.http import HttpResponse, Http404, HttpResponseRedirect
# from interface.models import Question
from .models import Site
from interface.forms import SubmissionForm
from django.shortcuts import render
from django.template import loader

# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     template = loader.get_template('index.html')
#     context = {
#         'latest_question_list': latest_question_list,
#     }
    
#     return HttpResponse(template.render(context, request))

def index(request):
    up_sites_list = Site.objects.filter(last_status__lte = 399)
    down_sites_list = Site.objects.filter(last_status__gt = 399).filter(last_status__lt = 999)
    offline_sites_list = Site.objects.filter(last_status = 999)
    
    context = {
        'up_sites_list': up_sites_list,
        'down_sites_list': down_sites_list,
        'offline_sites_list': offline_sites_list,
        }
    return render(request, 'index.html', context)
    
def thanks(request):
    return render(request, 'thanks.html')

def submission(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SubmissionForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            form.save()
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SubmissionForm()

    return render(request, 'submission.html', {'form': form})

# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/detail.html', {'question': question})
    
# def results(request, question_id):
#     response = "You're looking at the results of the question %s."
#     return HttpResponse(response % question_id)
    