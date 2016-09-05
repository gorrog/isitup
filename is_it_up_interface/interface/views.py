from django.http import HttpResponseRedirect
from .models import Site, Error
from interface.forms import SubmissionForm
from django.shortcuts import render

def index(request):
    # Any site with a status <= 399 is OK.
    up_sites_list = Site.objects.filter(last_status__lte = 399)
    print("up_sites_list is {}".format(up_sites_list))
    for my_site in up_sites_list:
        print("type(my_site) is {}".format(type(my_site)))
        print('site.first_checked is {}'.format(my_site.first_checked))
        error_percentage = get_error_percentage(my_site)
        setattr(my_site, "error_percentage", error_percentage)
    # If a site has a status code > 399 < 999, it indicates a problem
    down_sites_list = Site.objects.filter(last_status__gt = 399).filter(last_status__lt = 999)
    for my_site in down_sites_list:
        error_percentage = get_error_percentage(my_site)
        setattr(my_site, "error_percentage", error_percentage)
    # We use '999' as the code to signify that a site is completely unreachable
    offline_sites_list = Site.objects.filter(last_status = 999)
    for my_site in offline_sites_list:
        error_percentage = get_error_percentage(my_site)
        setattr(my_site, "error_percentage", error_percentage)
    context = {
        'up_sites_list': up_sites_list,
        'down_sites_list': down_sites_list,
        'offline_sites_list': offline_sites_list,
        }
    return render(request, 'index.html', context)

def get_error_percentage(my_site):
    print("We are in get_error_percentage now. my_site is {}".format(my_site))
    first_checked = my_site.first_checked
    last_checked = my_site.last_checked 
    time_checked_duration = last_checked - first_checked
    print("time checked duration is {}".format(time_checked_duration))
    error_count = len(Error.objects.filter(site=my_site.id))
    print("error count is {}".format(error_count))
    total_checks = time_checked_duration / my_site.schedule
    print("total_checks is {}".format(total_checks))
    error_percentage = (error_count/total_checks*100)
    return round(error_percentage, 2)
    
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

def contact(request):
    return render(request, 'contact.html')
    