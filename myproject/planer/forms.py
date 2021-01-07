from django.forms import ModelForm
from .models import event
from django import forms


class EventForm(ModelForm):

    class Meta:
        model = event
        fields = ['eday', 'emonth', 'etime', 'ename', 'etext']


class DelForm(ModelForm):
    id = forms.IntegerField()

    class Meta:
        model = event
        fields = ['userid', 'emonth', 'eday',  'ename', 'id']


class EditForm(ModelForm):
    new_etime = forms.TimeField()
    new_ename = forms.CharField(max_length=50)
    new_etext = forms.CharField(max_length=250)

    class Meta:
        model = event
        fields = ['ename', 'etext', 'userid', 'new_etime', 'new_ename', 'new_etext', 'emonth', 'eday']


class MoveForm(ModelForm):
    new_eday = forms.IntegerField()
    new_emonth = forms.CharField(max_length=50)

    class Meta:
        model = event
        fields = ['eday', 'new_eday', 'emonth', 'new_emonth', 'userid']


class GetEventForm(ModelForm):
    id = forms.IntegerField()
    interval = forms.CharField()

    class Meta:
        model = event
        fields = ['id', 'interval']
