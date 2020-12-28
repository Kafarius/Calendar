from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.urls import reverse
from .forms import EventForm, DelForm, EditForm, MoveForm, GetEventForm
from django.contrib import messages
import datetime
from datetime import date
from django.db.models import Count
from itertools import islice


from .models import event

def index(request):

    return render(request, 'base.html')


def signup(request):                                                        # USER REGISTRATION
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def signin(request):                                                        # USER LOG IN
    if request.user.is_authenticated:
        return render(request, 'base.html')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            form = AuthenticationForm(request.POST)
            return render(request, 'signin.html', {'form': form})
    else:
        form = AuthenticationForm()
        return render(request, 'signin.html', {'form': form})


def signout(request):                                                       # USER LOG OUT
    logout(request)
    return redirect('index')


def month_to_int(month):
    month_dict = {
        'January': '1',
        'February': '2',
        'March': '3',
        'April': '4',
        'May': '5',
        'June': '6',
        'July': '7',
        'August': '8',
        'September': '9',
        'October': '10',
        'November': '11',
        'December': '12',
    }
    value = month_dict[month]
    return value


def create_event(request):                                                   # EVENT CREATION

    week_days = {
        '0': 'Monday',
        '1': 'Tuesday',
        '2': 'Wednesday',
        '3': 'Thursday',
        '4': 'Friday',
        '5': 'Saturday',
        '6': 'Sunday',
    }
    form = EventForm()
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():

            event_obj = event(
                user = request.user,
                userid = request.user.id,
                eday = form.cleaned_data['eday'],
                emonth = form.cleaned_data['emonth'],
                etime = form.cleaned_data['etime'],
                ename = form.cleaned_data['ename'],
                etext = form.cleaned_data['etext'],
                edate = datetime.date(2021, int(month_to_int(form.cleaned_data['emonth'])), form.cleaned_data['eday']),
                eweekday = week_days[str(date(2021, int(month_to_int(form.cleaned_data['emonth'])), form.cleaned_data['eday']).weekday())]
                # password = form.cleaned_data['password'],
            )

            event_obj.save()

            # messages.success(request, 'Account has been created for ' + user)
            return redirect('planner', user = request.user)

        else:
            print(form.errors)
            return redirect('eventcreation')

    else:
        form = EventForm()


    context = {'form': form,

    }
    return render(request, 'eventcreation.html', context)


def delete_event(request):                                                  # EVENT DELETING
    form = DelForm()
    if request.method == 'POST':
        form = DelForm(request.POST)
        print(form.errors)
        if form.is_valid():
            userid = form.cleaned_data['userid']
            emonth = form.cleaned_data['emonth']
            eday = form.cleaned_data['eday']
            ename = form.cleaned_data['ename']
            event_obj = event.objects.filter(userid=userid, emonth=emonth, eday=eday,  ename=ename)
            event_obj.delete()
    return redirect('planner', user = request.user)


def edit_event(request):
    form = EditForm()
    if request.method == 'POST':
        form = EditForm(request.POST)
        print(form.errors)
        if form.is_valid():

            ename = form.cleaned_data['ename']
            etext = form.cleaned_data['etext']
            userid = form.cleaned_data['userid']
            new_etime = form.cleaned_data['new_etime']
            new_ename = form.cleaned_data['new_ename']
            new_etext = form.cleaned_data['new_etext']

            event_edited = event.objects.filter(userid=userid, ename=ename, etext=etext)
            event_edited.update(etime=new_etime, ename=new_ename, etext=new_etext)

    return redirect('planner', user=request.user)


def move_event(request):
    week_days = {
        '0': 'Monday',
        '1': 'Tuesday',
        '2': 'Wednesday',
        '3': 'Thursday',
        '4': 'Friday',
        '5': 'Saturday',
        '6': 'Sunday',
    }
    form = MoveForm
    if request.method == 'POST':
        form = MoveForm(request.POST)
        print(form.errors)
        if form.is_valid():
            userid = form.cleaned_data['userid']
            eday = form.cleaned_data['eday']
            emonth = form.cleaned_data['emonth']
            new_eday = form.cleaned_data['new_eday']
            new_emonth = form.cleaned_data['new_emonth']
            new_edate = datetime.date(2021, int(month_to_int(form.cleaned_data['new_emonth'])), form.cleaned_data['new_eday'])
            new_eweekday = week_days[str(date(2021, int(month_to_int(form.cleaned_data['new_emonth'])), form.cleaned_data['new_eday']).weekday())]
            event_moved = event.objects.filter(userid=userid, eday=eday, emonth=emonth)
            event_moved.update(eday=new_eday, emonth=new_emonth, edate=new_edate, eweekday=new_eweekday)

    return redirect('planner', user=request.user)


def make_monthly(request):
    week_days = {
        '0': 'Monday',
        '1': 'Tuesday',
        '2': 'Wednesday',
        '3': 'Thursday',
        '4': 'Friday',
        '5': 'Saturday',
        '6': 'Sunday',
    }
    form = GetEventForm()
    if request.method == 'POST':
        form = GetEventForm(request.POST)
        print(form.errors)
        if form.is_valid():
            id = form.cleaned_data['id']
            ev = event.objects.get(id = id)
            print(ev.ename)
            time = datetime.datetime.now()
            size = 13

            month_dict = {
                '1': 'January',
                '2': 'February',
                '3': 'March',
                '4': 'April',
                '5': 'may',
                '6': 'June',
                '7': 'July',
                '8': 'August',
                '9': 'September',
                '10': 'October',
                '11': 'November',
                '12': 'December',
            }

            objs = (event(
                userid=ev.userid,
                user = ev.user,
                eday = ev.eday,
                emonth = month_dict[str(i)],
                etime = ev.etime,
                ename = ev.ename,
                etext = ev.etext,
                ecreationdate = time.strftime("%X"),
                edate = '2021-' + str(i) + '-' + str(ev.eday),
                eweekday = week_days[str(date(2021, int(i), ev.eday).weekday())]) for i in range(1, 13, 1))
            while True:
                batch = list(islice(objs, size))
                if not batch:
                    break
                event.objects.bulk_create(batch, size)

    return redirect('planner', user=request.user)


def show_planner(request, user):
    events = event.objects.all().filter(user = user).order_by('edate')
    months = event.objects.raw('SELECT * FROM planer_event WHERE user = %s GROUP BY emonth ORDER BY edate', [user])
    context = {
        'user': user,
        'events': events,
        'months': months,
    }

    return render(request, 'planner.html', context)


def show_month(request, user, month):
    events = event.objects.all().filter(user=user, emonth=month).order_by('etime')
    days = events.values('eday', 'eweekday').annotate(ecount=Count('eday')).order_by('edate')

    context = {
        'user': user,
        'events': events,
        'month': month,
        'days': days,


    }
    return render(request, 'month.html', context)
