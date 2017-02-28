# -*- coding=utf-8 -*-
from django.db import models

# Create your models here.


class LoginLog(models.Model):
    Loginuser = models.CharField(max_length=16,default='-')
    Logintime = models.CharField(max_length=32,blank=True,null=True,default='-')
    Logouttime = models.CharField(max_length=32,blank=True,null=True,default='-')
    Logaction = models.CharField(max_length=32,default='-')
    LogIP = models.CharField(max_length=16,default='0.0.0.0')

class ActionLog(models.Model):
	Actionuser = models.CharField(max_length=16)
	Actiontime = models.CharField(max_length=32)
	Actiontype = models.CharField(max_length=16)
	Actionmodule = models.CharField(max_length=16)
	Actioninfo = models.CharField(max_length=128)
