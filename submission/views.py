from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.cache import never_cache
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.db.models import Sum

from PIL import Image
from datetime import datetime

from submission.models import Entry, JudgeNote
from submission.forms import EntryForm


def vis_thumbnail(visimage):
    """
    Saves a bvisualization image file with alternative sizes to the given path in MEDIA_ROOT.

    """
    tn = Image.open(visimage.path)
    tn.thumbnail((580, 386), Image.ANTIALIAS)
    tnpath = '%s_tn.png' % (visimage.path[:-4])
    tn.save(tnpath, 'PNG', optimize=True)

@never_cache
def add(request):
    """ Add new entry before deadline """

    if datetime.now() > datetime.strptime(settings.DEADLINE_SUBMISSION, '%Y-%m-%d %H:%M'):
        return redirect('/')
    else:
        # save form
        if request.method == 'POST':
            new_entry = Entry()
            entryform = EntryForm(request.POST, request.FILES, instance=new_entry)
            if entryform.is_valid():
                if request.user.is_authenticated():
                    new_entry.user = request.user
                entryform.save()
                vis_thumbnail(new_entry.screenshot)
                return render_to_response('submission/thankyou.html', locals(), context_instance=RequestContext(request))
        # show empty form
        else:
            user = request.user
            entryform = EntryForm()
        return render_to_response('submission/add.html', locals(), context_instance=RequestContext(request))

def get_first_obj(qs):
    if qs:
        return qs[0]
    else:
        return False

@never_cache
def detail(request, id):
    """ Render detail page for an entry """
    entry = get_object_or_404(Entry, pk=id)
    user = request.user
    judge = user.groups.filter(name='judges').exists()

    if judge:
        try:
            judgenote = JudgeNote.objects.get(user=user, entry=entry)
        except ObjectDoesNotExist:
            judgenote = None;

    if user.is_staff:
        previous = get_first_obj(Entry.objects.filter(id__lt=id).reverse())
        next = get_first_obj(Entry.objects.filter(id__gt=id))
    else:
        previous = get_first_obj(Entry.objects.filter(id__lt=id, approved=True).reverse())
        next = get_first_obj(Entry.objects.filter(id__gt=id, approved=True))
    
    return render_to_response('submission/detail.html', locals(), context_instance=RequestContext(request))

@login_required
@never_cache
def rate(request, id):
    """ Handler for an AJAX POST from a detail page for a rating score. """

    if request.method == "POST":
        entry = get_object_or_404(Entry.objects, pk=id)
        try:
            # add rating
            entry.userrating.add(score=request.POST['score'], user=request.user, ip_address=request.META['REMOTE_ADDR'])
            return HttpResponse(status=200)
        except:
            return HttpResponse(status=500)

@login_required
@never_cache
def judgerate(request, id):
    """ Handler for an AJAX POST from a detail page for a rating score. """
    judge = request.user.groups.filter(name='judges').exists()
    if request.method == "POST" and judge:
        entry = get_object_or_404(Entry.objects, pk=id)
        try:
            # add rating
            entry.judgerating.add(score=request.POST['score'], user=request.user, ip_address=request.META['REMOTE_ADDR'])
            return HttpResponse(status=200)
        except:
            return HttpResponse(status=500)
    else:
        return HttpResponse(status=500)

@login_required
@never_cache
def judgenote(request):
    """ Handler for an AJAX POST from a detail page for a rating score. """
    user = request.user
    judge = user.groups.filter(name='judges').exists()
    entry = Entry.objects.get(pk=request.POST['entry']) 
    if request.method == "POST" and judge:
        try:
            if 'id' in request.POST:
                judgenote = JudgeNote.objects.get(pk=request.POST['id'])
            else:
                judgenote = JudgeNote()

            judgenote.note = request.POST['note']
            judgenote.entry = entry
            judgenote.user = user
            judgenote.save()
            return HttpResponse(status=200)
        except:
            return HttpResponse(status=500)
    else:
        return HttpResponse(status=500)

@staff_member_required
def approve(request, id):
    entry = get_object_or_404(Entry, pk=id)
    try:
        entry.approved = True
        entry.save()
        return HttpResponse(status=200)
    except:
        return HttpResponse(status=500)

def leaderboard(request):
    """ 
        Show all entries, sorted by rating
        FIXME: sorting should ideally happen in DB
    """

    entries = Entry.objects.all().filter(approved=True, userrating_votes__gt=0)

    if request.user.is_staff:
        entries = entries.filter(judgerating_votes__gt=0)
        entries = list(entries)
        entries.sort(key=lambda x: x.judgerating.get_rating(), reverse=True)
    else:
        userrating_votes_aggr = entries.aggregate(Sum('userrating_votes'))
        userrating_votes_sum = userrating_votes_aggr['userrating_votes__sum']
        entries = list(entries)
        entries.sort(key=lambda x: x.userrating.get_rating(), reverse=True)

    return render_to_response('submission/leaderboard.html', locals(), context_instance=RequestContext(request))

