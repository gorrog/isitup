from django.http import HttpResponseRedirect
from .models import Site
from interface.forms import SubmissionForm
from django.shortcuts import render

def index(request):
    # Any site with a status <= 399 is OK.
    up_sites_list = Site.objects.filter(last_status__lte = 399)
    # If a site has a status code > 399 < 999, it indicates a problem
    down_sites_list = Site.objects.filter(last_status__gt = 399).filter(last_status__lt = 999)
    # We use '999' as the code to signify that a site is completely unreachable
    offline_sites_list = Site.objects.filter(last_status = 999)
    context = {
        'up_sites_list': up_sites_list,
        'down_sites_list': down_sites_list,
        'offline_sites_list': offline_sites_list,
        }
    return render(request, 'index.html', context)

# This page thanks a user for their submission of a site
def thanks(request):
    return render(request, 'thanks.html')

# Page for submitting a site. 
def submission(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SubmissionForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SubmissionForm()

    return render(request, 'submission.html', {'form': form})

