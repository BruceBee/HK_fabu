#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import HttpResponse,render,HttpResponseRedirect 
from public.publicfunction import GetUserAuth


def haproxyedit(request):

    if 'LoginName' not in request.session:
        # 用户未登录跳转
        return HttpResponseRedirect('/login')

    if request.method == 'GET':
        LoginName = request.session['LoginName']

        have_publish,have_review,have_test = GetUserAuth(LoginName)
        return render(request, "haproxyedit/haproxyedit.html", {'LoginName': LoginName,
        											'navbar':'Haproxy配置',
        											'url':'/haproxyedit/',
        											'have_publish':have_publish,
        											'have_review':have_review,
        											'have_test':have_test})
    else:
        pass