#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import HttpResponseRedirect
from public.publicfunction import *
from public.publicvar import *
import multiprocessing
import commands
import os
import json


def check_and_read_log(d, logfilenames):
    d['task'] = {}
    for logfilename in logfilenames:
        strip_list = logfilename.strip('/').split('/')

        nfs_path = strip_list[0]
        serverip = strip_list[1]
        project_name = strip_list[2]
        logfile = strip_list[-1] if len(strip_list) == 5 else "catalina.out"
        print strip_list
        path_with_serverip = '/' + nfs_path + '/' + serverip
        path_with_projectname = path_with_serverip + '/' + project_name
        path_full = path_with_projectname + '/logs/' + logfile
        mount_path = '/' + nfs_path
        mount_cmd = 'sudo mount %s:%s %s' % (serverip, mount_path, path_with_serverip)

        if os.path.isfile(path_full):
            status, logoutput = commands.getstatusoutput('tail -100 %s' % path_full)
            foo = d['task']
            foo[serverip] = logoutput
            d['task'] = foo

        else:
            if not os.path.exists(path_with_serverip):
                # 检查以IP命名的文件夹是否存在
                os.makedirs(path_with_serverip)

            dir_list = os.listdir(path_with_serverip)
            if len(dir_list) > 0 and project_name not in dir_list:
                # 对应服务器logs目录已经挂载但无对应项目日志
                foo = d['task']
                foo[serverip] = '无此项目模块的日志信息！\n如果此项目模块在日志查看功能上线之前就已部署，则需要全新部署一次来激活功能！'
                d['task'] = foo

            elif len(dir_list) == 0:
                status, output = commands.getstatusoutput(mount_cmd)
                if status != 0:
                    foo = d['task']
                    foo[serverip] = output
                    d['task'] = foo

            if os.path.isfile(path_full):
                status, logoutput = commands.getstatusoutput('tail -100 %s' % path_full)
                foo = d['task']
                foo[serverip] = logoutput
                d['task'] = foo
            else:
                foo = d['task']
                foo[serverip] = '日志文件不存在！'
                d['task'] = foo
    return



def showlogs(request):
    # 用户未登录跳转
    if 'LoginName' not in request.session:
        return HttpResponseRedirect('/login')
    if request.method == 'GET':
        have_publish,have_review,have_test = GetUserAuth(request.session['LoginName'])
        return render(request, "showlogs/showlogs.html", {'project_lists': read_project_name(),
                                                 'LoginName': request.session['LoginName'],
                                                 'navbar':'日志查看',
                                                 'url':'/showlogs/',
                                                 'have_publish':have_publish,
                                                 'have_review':have_review,
                                                 'have_test':have_test})

    else:
        project_name = request.POST['project_name']
        logfilename = request.POST['logfilename']
        getserver = read_project_name(project_name)
        tmppath = os.path.join('/logs', logfilename)
        path_lists = [os.path.join(TOMCAT_LOG_PATH_MOUNT, ip) + '/tomcat_' + project_name + tmppath for ip in getserver]

        p = multiprocessing.Pool(len(path_lists))       # 使用多进程
        m = multiprocessing.Manager()
        d = m.dict()
        p.apply_async(check_and_read_log(d, path_lists))
        # logs = p.map(check_and_read_log, path_lists)        # 使用多进程
        p.close()
        p.join()

        logs = d['task']

        return HttpResponse(json.dumps(logs))


