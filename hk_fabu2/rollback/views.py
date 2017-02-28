#!/usr/bin/env python
# -*- coding:utf-8 -*-
from public.publicvar import *
from public.publicfunction import read_project_name
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import HttpResponse
from django.shortcuts import render
import commands
import json


def rollback(request):
    if 'LoginName' not in request.session:
        # 用户未登录跳转
        return HttpResponseRedirect('/login')
    if request.POST:
        # 操作提交
        pass
    else:
        return render(request, 'rollback.html', {'project_lists': read_project_name()})


def get_backup_name(request):
    if 'LoginName' not in request.session:
        # 用户未登录跳转
        return HttpResponseRedirect('/login')
    project_name = request.GET['project_name']
    server_lists = read_project_name(project_name)
    backup_name = {}
    for i in server_lists:
        status, output = commands.getstatusoutput("ssh tomcat@%s 'ls /opt/backup/%s_*'" % (i, project_name))
        if status == 0:
            backup_name[i] = [x.split('/')[-1] for x in output.split('\n')]
    return HttpResponse(json.dumps([project_name, backup_name]))
