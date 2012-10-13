from django.contrib.auth import logout
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from submission.models import Entry

from tastypie.models import ApiKey

def home(request):
	entries = Entry.objects.filter(approved=True).reverse()
	if entries:
		lastentry = entries[0]
	return render_to_response('index.html', locals(), context_instance=RequestContext(request))

def logout_view(request):
    logout(request)
    return redirect('/')

@login_required
def data_api(request):
    apikey = get_object_or_404(ApiKey, user=request.user)
    user = request.user
    return render_to_response('data-api.html', locals(), context_instance=RequestContext(request))
