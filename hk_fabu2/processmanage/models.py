from django.db import models

# Create your models here.

class ProcessInfo(models.Model):
    HostIP = models.CharField(max_length=16,default='-')
    USER = models.CharField(max_length=16,blank=True,null=True,)
    PID = models.CharField(max_length=8,blank=True,null=True,)
    CPU = models.CharField(max_length=8,blank=True,null=True,)
    MEM = models.CharField(max_length=8,blank=True,null=True,)
    START = models.CharField(max_length=16,blank=True,null=True,)
    TIME = models.CharField(max_length=16,blank=True,null=True,)
    COMMAND = models.CharField(max_length=2048,blank=True,null=True,)
    STAT = models.CharField(max_length=8,blank=True,null=True,)
    CollectTime = models.CharField(max_length=20,blank=True,null=True,default='1970-01-01 00:00:00')
