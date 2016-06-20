from datetime import datetime
from decimal import Decimal
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.timezone import get_current_timezone

from .models import Activity, Event

# Create your views here.

def index(request):
    if not request.user.is_authenticated():
        return render(request, 'login.html')
    activities = []
    for activity in request.user.activities.filter(is_active=True):
        count = activity.events.all().count()
        latest = None
        if count:
            latest = activity.events.all().order_by('-start_at')[0]
            if latest.end_at:
                latest = None
        row = (activity, count, latest)
        activities.append(row)
    return render(request, 'index.html', {'activities': activities})


@login_required
def archive(request):
    activities = []
    for activity in request.user.activities.filter(is_active=False):
        count = activity.events.all().count()
        row = (activity, count)
        activities.append(row)
    return render(request, 'archive.html', {'activities': activities})


@login_required
def add(request):
    if request.method == 'GET':
        return render(request, 'activitynew.html')
    try:
        name = request.POST['name']
        if not name:
            raise Exception('Activity name cannot be empty.')
        count = Activity.objects.filter(owner=request.user, name=name).count()
        if count:
            raise Exception('Activity name should be unique.')
        activity = Activity()
        activity.name = name
        activity.is_point = 'point' in request.POST
        activity.owner = request.user
        activity.save()
        return HttpResponseRedirect(reverse('index'))
    except Exception as ex:
        context = {'success': False, 'message': str(ex)}
        return render(request, 'msg.html', context)


@login_required
def showactivity(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)
    if activity.owner != request.user:
        return render(request, 'msg.html', {'success': False, 'message': 'Cannot view the activity'})
    return render(request, 'activitydetail.html', {'activity': activity})


@login_required
def updateactivity(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)
    if activity.owner != request.user:
        return render(request, 'msg.html', {'success': False, 'message': 'Cannot update the activity'})
    try:
        name = request.POST['name']
        if name != activity.name:
            if not name:
                raise Exception('Activity name cannot be empty.')
            count = Activity.objects.filter(owner=request.user, name=name).count()
            if count:
                raise Exception('Activity name should be unique.')
            activity.name = name
        activity.description = request.POST['description']
        activity.is_point = 'point' in request.POST
        activity.is_active = 'active' in request.POST
        activity.save()
        if activity.is_active:
            return HttpResponseRedirect(reverse('index'))
        return HttpResponseRedirect(reverse('archive'))
    except Exception as ex:
        context = {'success': False, 'message': str(ex)}
        return render(request, 'msg.html', context)


@login_required
def deleteactivity(request, activity_id):
    if request.method != 'POST':
        return render(request, 'msg.html', {'success': False, 'message': 'Wrong method'})
    activity = get_object_or_404(Activity, pk=activity_id)
    if activity.owner != request.user:
        return render(request, 'msg.html', {'success': False, 'message': 'Cannot delete the activity'})
    is_active = activity.is_active
    activity.delete()
    if is_active:
        return HttpResponseRedirect(reverse('index'))
    return HttpResponseRedirect(reverse('archive'))


@login_required
def startactivity(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)
    if activity.owner != request.user:
        return render(request, 'msg.html', {'success': False, 'message': 'Cannot start the activity'})
    if not activity.is_active:
        return render(request, 'msg.html', {'success': False, 'message': 'Cannot start the activity in archive'})
    event = Event()
    event.activity = activity
    event.start_at = timezone.now()
    event.save()
    return HttpResponseRedirect(reverse('index'))


@login_required
def startactivityat(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)
    if activity.owner != request.user:
        return render(request, 'msg.html', {'success': False, 'message': 'Cannot start the activity'})
    if not activity.is_active:
        return render(request, 'msg.html', {'success': False, 'message': 'Cannot start the activity in archive'})
    if request.method == 'GET':
        event = Event()
        event.activity = activity
        event.start_at = timezone.now()
        return render(request, 'eventstart.html', {'event': event})
    try:
        event = Event()
        event.activity = activity
        start_at = request.POST['start'].replace('a.m.', 'AM').replace('p.m.', 'PM') + ' CST'
        event.start_at = datetime.strptime(start_at, '%B %d, %Y, %I:%M %p %Z')
        data = request.POST['data'].strip()
        if data:
            event.data = Decimal(data)
        else:
            event.data = None
        event.save()
        return HttpResponseRedirect(reverse('index'))
    except Exception as ex:
        context = {'success': False, 'message': str(ex)}
        return render(request, 'msg.html', context)


@login_required
def endactivity(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if event.activity.owner != request.user:
        return render(request, 'msg.html', {'success': False, 'message': 'Cannot end the activity'})
    if not event.activity.is_active:
        return render(request, 'msg.html', {'success': False, 'message': 'Cannot end the activity in archive'})
    event.end_at = timezone.now()
    event.save()
    return HttpResponseRedirect(reverse('index'))


@login_required
def endactivityat(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if event.activity.owner != request.user:
        return render(request, 'msg.html', {'success': False, 'message': 'Cannot end the activity'})
    if not event.activity.is_active:
        return render(request, 'msg.html', {'success': False, 'message': 'Cannot end the activity in archive'})
    if request.method == 'GET':
        event.end_at = timezone.now()
        return render(request, 'eventend.html', {'event': event})
    try:
        start_at = request.POST['start'].replace('a.m.', 'AM').replace('p.m.', 'PM') + ' CST'
        event.start_at = datetime.strptime(start_at, '%B %d, %Y, %I:%M %p %Z')
        if not event.activity.is_point:
            end_at = request.POST['end'].replace('a.m.', 'AM').replace('p.m.', 'PM') + ' CST'
            event.end_at = datetime.strptime(end_at, '%B %d, %Y, %I:%M %p %Z')
            if start_at > end_at:
                raise Exception('Start time must be before end time')
        data = request.POST['data'].strip()
        if data:
            event.data = Decimal(data)
        else:
            event.data = None
        event.save()
        return HttpResponseRedirect(reverse('index'))
    except Exception as ex:
        context = {'success': False, 'message': str(ex)}
        return render(request, 'msg.html', context)


@login_required
def showevents(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)
    if activity.owner != request.user:
        return render(request, 'msg.html', {'success': False, 'message': 'Cannot show records in the activity'})
    events = list(activity.events.all().order_by('-start_at'))
    return render(request, 'events.html', {'activity': activity, 'events': events})


@login_required
def updateevent(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if event.activity.owner != request.user:
        return render(request, 'msg.html', {'success': False, 'message': 'Cannot edit the event'})
    if not event.activity.is_active:
        return render(request, 'msg.html', {'success': False, 'message': 'Cannot update the archived activity'})
    if request.method == 'GET':
        return render(request, 'eventdetail.html', {'event': event})
    try:
        start_at = request.POST['start'].replace('a.m.', 'AM').replace('p.m.', 'PM') + ' CST'
        event.start_at = datetime.strptime(start_at, '%B %d, %Y, %I:%M %p %Z')
        if not event.activity.is_point:
            end_at = request.POST['end'].replace('a.m.', 'AM').replace('p.m.', 'PM') + ' CST'
            event.end_at = datetime.strptime(end_at, '%B %d, %Y, %I:%M %p %Z')
            if start_at > end_at:
                raise Exception('Start time must be before end time')
        data = request.POST['data'].strip()
        if data:
            event.data = Decimal(data)
        else:
            event.data = None
        event.save()
        return HttpResponseRedirect(reverse('showevents', args=(event.activity.id,)))
    except Exception as ex:
        context = {'success': False, 'message': str(ex)}
        return render(request, 'msg.html', context)


@login_required
def deleteevent(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if event.activity.owner != request.user:
        return render(request, 'msg.html', {'success': False, 'message': 'Cannot edit the event'})
    if request.method == 'GET':
        return render(request, 'eventdetail.html', {'event': event})
    return render(request, 'eventdetail.html', {'event': event})


def userlogin(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
    return render(request, 'msg.html', {'success': False, 'message': 'Cannot login! Incorrect username or password.'})


def userlogout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
