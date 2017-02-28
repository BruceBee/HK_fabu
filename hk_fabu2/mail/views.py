# -*- coding:utf-8 -*-
from django.shortcuts import render,HttpResponse, render_to_response
from public.publicfunction import *
# from index.models import UserLoginInfo

# Create your views here.
# def GetUserAuth(user):
# 	UserObject = UserLoginInfo.objects.get(user=user)
# 	return UserObject.have_publish,UserObject.have_review,UserObject.have_test

def index(request):
	have_publish,have_review,have_test = GetUserAuth(request.session['LoginName'])
	return render(request,'mail/mailsetting.html',{'LoginName': request.session['LoginName'],
												   'navbar':'通知设置',
												   'url':'/mail/',
												   'have_publish':have_publish,
												   'have_review':have_review,
												   'have_test':have_test})
