# -*- coding:utf-8 -*-
from django.shortcuts import render,HttpResponse, render_to_response

# Create your views here.

def PublishList(request):
    return render(request,'publishlist.html',{'LoginName': request.session['LoginName']})
