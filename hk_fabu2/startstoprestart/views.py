#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import HttpResponseRedirect, HttpResponse, render
from public.publicfunction import *
from public.publicvar import *
from index.models import Logging
import commands
import json


OPERATION_CMD = "ansible-playbook %s --extra-vars 'project_host=%s project_name=%s' -v -t %s"


def runplaybook(project_name, serverlist_operation, operation):
    project_server_list = read_project_name(project_name)
    except_server_cmd = ''
    if len(project_server_list) > len(serverlist_operation):
        except_server = list(set(project_server_list) - set(serverlist_operation))
        except_server_cmd = ''.join(':!'+i for i in except_server)

    project_host = project_name + except_server_cmd
    status, output = commands.getstatusoutput(OPERATION_CMD % (operation_yml_path, project_host, project_name, operation))
    return status, output


def startstoprestart(request):
    """
    发布提交页面主处理函数
    :param request:
    :return:
    """

    if 'LoginName' not in request.session:
        # 用户未登录跳转
        return HttpResponseRedirect('/login')

    if request.POST:

        serverlist_operation = request.POST.getlist('serverlist')
        project_name = request.POST['project_name']
        operation = request.POST['operation']

        if len(serverlist_operation) == 0:
            return HttpResponse('<h1>未选择任何服务器</h1>')

        status, output = runplaybook(project_name, serverlist_operation, operation)
        log = Logging(operation='StartStopRestart', user=request.session['LoginName'],
                      project_name=project_name, dest_server=serverlist_operation, log_date=output, state='Done')
        log.save()
        return HttpResponse('<h1>操作成功</h1><br /><a href="">返回</a>')
    else:
        if 'project_name' in request.GET:
            if 'operation' not in request.GET:
                return HttpResponse(json.dumps(read_project_name(request.GET['project_name'])))
            else:
                pass
        else:
            have_publish,have_review,have_test = GetUserAuth(request.session['LoginName'])
            return render(request, 'startstoprestart/startstoprestart.html', {'project_lists': read_project_name(),
                                                             'LoginName': request.session['LoginName'],
                                                             'navbar':'起停控制',
                                                             'url':'/startstoprestart/',
                                                             'have_publish':have_publish,
                                                             'have_review':have_review,
                                                             'have_test':have_test})

