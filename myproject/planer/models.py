from django.db import models
import datetime


class event(models.Model):

    id = models.AutoField(primary_key=True)
    userid = models.IntegerField()
    user = models.CharField(max_length=50)
    eday = models.IntegerField()
    emonth = models.CharField(max_length=50)
    etime = models.TimeField()
    ename = models.CharField(max_length=50)
    etext = models.TextField(max_length=250)
    ecreationdate = models.DateTimeField(auto_now=True)
    edate = models.DateField()
    eweekday = models.CharField(max_length=50)

    objects = models.Manager()