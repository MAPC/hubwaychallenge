from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse

from submission.models import Entry
from submission.forms import EntryForm


def add(request):
    """ Add new entry """

    # save form
    if request.method == 'POST':
        new_entry = Entry()
        entryform = EntryForm(request.POST, request.FILES, instance=new_entry)
        if entryform.is_valid():
            if request.user.is_authenticated():
                new_entry.user = request.user
            entryform.save()
            # TODO: resize screenshot
            return render_to_response('submission/thankyou.html', locals(), context_instance=RequestContext(request))
    # show empty form
    else:
        user = request.user
        entryform = EntryForm()

    return render_to_response('submission/add.html', locals(), context_instance=RequestContext(request))


def detail(request, id):
    """ Render detail page for an entry """
    entry = get_object_or_404(Entry, pk=id)
    return render_to_response('submission/detail.html', locals(), context_instance=RequestContext(request))

