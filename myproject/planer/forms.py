from django.forms import ModelForm
from .models import event
from django import forms


class EventForm(ModelForm):

    class Meta:
        model = event
        fields = ['eday', 'emonth', 'etime', 'ename', 'etext']


class IdForm(ModelForm):
    id = forms.IntegerField()

    class Meta:
        model = event
        fields = ['id']


class EditForm(IdForm):
    new_etime = forms.TimeField()
    new_ename = forms.CharField(max_length=50)
    new_etext = forms.CharField(max_length=250)

    class Meta:
        model = event
        fields = ['id', 'new_etime', 'new_ename', 'new_etext']


class MoveForm(IdForm):
    new_eday = forms.IntegerField()
    new_emonth = forms.CharField(max_length=50)

    class Meta:
        model = event
        fields = ['id', 'new_eday', 'new_emonth']


class GetEventForm(IdForm):
    interval = forms.CharField()

    class Meta:
        model = event
        fields = ['id', 'interval']


class FeedbackForm(forms.Form):
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)


