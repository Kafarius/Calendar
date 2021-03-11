from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.urls import reverse
from .forms import EventForm, IdForm, EditForm, MoveForm, GetEventForm, FeedbackForm
from django.contrib import messages
import datetime
from datetime import date
from django.db.models import Count
from itertools import islice
from django.core.mail import send_mail
import smtplib


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


def month_converter(month):
    month_dict = {
        'January': 1,
        'February': 2,
        'March': 3,
        'April': 4,
        'May': 5,
        'June': 6,
        'July': 7,
        'August': 8,
        'September': 9,
        'October': 10,
        'November': 11,
        'December': 12,
    }
    if isinstance(month, str):
        result = month_dict[month]
    else:
        for key, value in month_dict.items():
            if month == value:
                result = key
    return result


def weekday(day):
    week_days = {
        '0': 'Monday',
        '1': 'Tuesday',
        '2': 'Wednesday',
        '3': 'Thursday',
        '4': 'Friday',
        '5': 'Saturday',
        '6': 'Sunday',
    }
    day_name = week_days[day]
    return day_name


def days_in_month(month):
    days = 0
    if month in ['January', 'March', 'May', 'July', 'August', 'October', 'December']:
        days = 31
    elif month in ['April', 'June', 'September', 'November']:
        days = 30
    elif month == 'February':
        days = 28
    return days


def create_event(request):                                                   # EVENT CREATION

    # form = EventForm()
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
                edate = datetime.date(2021, int(month_converter(form.cleaned_data['emonth'])), form.cleaned_data['eday']),
                eweekday = weekday(str(date(2021, int(month_converter(form.cleaned_data['emonth'])), form.cleaned_data['eday']).weekday()))
            )
            event_obj.save()
            # messages.success(request, 'Event has been created')
            return redirect('planner', user=request.user)
        else:
            print(form.errors)
            return redirect('eventcreation')
    else:
        form = EventForm()
    context = {'form': form}
    return render(request, 'eventcreation.html', context)


def delete_event(request):                                                  # EVENT DELETING
    form = IdForm()
    if request.method == 'POST':
        form = IdForm(request.POST)
        print(form.errors)
        if form.is_valid():
            id = form.cleaned_data['id']
            event_obj = event.objects.filter(id=id)
            event_obj.delete()
    return redirect('planner', user=request.user)


def edit_event(request):
    form = EditForm()
    if request.method == 'POST':
        form = EditForm(request.POST)
        print(form.errors)
        if form.is_valid():

            id = form.cleaned_data['id']
            new_etime = form.cleaned_data['new_etime']
            new_ename = form.cleaned_data['new_ename']
            new_etext = form.cleaned_data['new_etext']

            event.objects.filter(id=id).update(etime=new_etime, ename=new_ename, etext=new_etext)

    return redirect('planner', user=request.user)


def move_event(request):
    form = MoveForm
    if request.method == 'POST':
        form = MoveForm(request.POST)
        print(form.errors)
        if form.is_valid():
            id = form.cleaned_data['id']
            new_eday = form.cleaned_data['new_eday']
            new_emonth = form.cleaned_data['new_emonth']
            new_edate = datetime.date(2021, int(month_converter(form.cleaned_data['new_emonth'])), form.cleaned_data['new_eday'])
            new_eweekday = weekday(str(date(2021, int(month_converter(form.cleaned_data['new_emonth'])), form.cleaned_data['new_eday']).weekday()))
            event.objects.filter(id=id).update(eday=new_eday, emonth=new_emonth, edate=new_edate, eweekday=new_eweekday)




    return redirect('planner', user=request.user)


def make_cyclical(request):

    form = GetEventForm()
    if request.method == 'POST':
        form = GetEventForm(request.POST)

        if form.is_valid():
            id = form.cleaned_data['id']
            interval = form.cleaned_data['interval']
            ev = event.objects.get(id=id)
            time = datetime.datetime.now()

            if interval == 'Monthly':
                size = 13
                objs = (event(
                    userid=ev.userid,
                    user=ev.user,
                    eday=ev.eday,
                    emonth=month_converter(i),
                    etime=ev.etime,
                    ename=ev.ename,
                    etext=ev.etext,
                    ecreationdate=time.strftime("%X"),
                    edate='2021-' + str(i) + '-' + str(ev.eday),
                    eweekday=weekday(str(date(2021, int(i), ev.eday).weekday()))) for i in range(2, 13, 1))

            elif interval == 'Daily':
                size = days_in_month(ev.emonth) - ev.eday
                objs = (event(
                    userid=ev.userid,
                    user=ev.user,
                    eday=i,
                    emonth=ev.emonth,
                    etime=ev.etime,
                    ename=ev.ename,
                    etext=ev.etext,
                    ecreationdate=time.strftime("%X"),
                    edate='2021-' + str(month_converter(str(ev.emonth))) + '-' + str(i),
                    eweekday=weekday(str(date(2021, int(month_converter(str(ev.emonth))), i).weekday()))) for i in range(ev.eday + 1, days_in_month(ev.emonth) + 1, 1))

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


def show_contact(request):
    form = FeedbackForm()
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            mailFrom = email
            mailTo = ['eplan.feedback@gmail.com']
            mailSubject = "Event move success!"
            mailBody = '''
                        From: {}
                        \n{}
                        '''.format(mailFrom, message)
            user = 'eplan.feedback@gmail.com'
            password = 'eplanfeedback123'

            if "eplan.feedback@gmail.com" in str(email):
                messages.error(request, "Hey, that's my email! Please use yours.")
            else:
                try:
                    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                    server.ehlo()
                    server.login(user, password)
                    server.sendmail(user, mailTo, mailBody)
                    server.close()
                    messages.success(request, 'Message has been sent!')
                except:
                    messages.error(request, 'Error!')
    else:
            form = FeedbackForm()
    context = {
        'form': form,
    }
    return render(request, 'contact.html', context)



