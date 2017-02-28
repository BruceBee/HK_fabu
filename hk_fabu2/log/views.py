# -*- coding:utf-8 -*-
from django.shortcuts import render,HttpResponse, render_to_response
from django.db.models import Q
from log.models import LoginLog,ActionLog
#from index.models import UserLoginInfo
from usermanage.models import UserInfo
import json,time


curr_date = time.strftime('%Y-%m-%d %H:%M:%S')#获取当前时间字符串

# Create your views here.

def GetUserAuth(user):
	UserObject = UserInfo.objects.get(user=user)
	return UserObject.have_publish,UserObject.have_review,UserObject.have_test

def index(request):
	have_publish,have_review,have_test = GetUserAuth(request.session['LoginName'])
	return render(request,'log/loginfo.html',{'LoginName': request.session['LoginName'],
											  'navbar':'系统日志',
											  'url':'/log/',
											  'have_publish':have_publish,
											  'have_review':have_review,
											  'have_test':have_test})



def GetLoginList(request):
	s_page = request.POST.get('s_page','')
	page_size = request.POST.get('page_size','')
	LogQsetList = LoginLog.objects.values().order_by('-id')[(int(s_page)-1)*int(page_size):int(s_page)*int(page_size)]
	data = "{\"LogQsetList\":"+json.dumps(list(LogQsetList))+"}"

	return HttpResponse(data)


def GetLoginPageCount(request):
	page_total = LoginLog.objects.all().count()
	return HttpResponse(page_total)



def GetActionList(request):
	s_page = request.POST.get('s_page','')
	page_size = request.POST.get('page_size','')
	ActionQsetList = ActionLog.objects.all().values().order_by('-id')[(int(s_page)-1)*int(page_size):int(s_page)*int(page_size)]
	data = "{\"ActionQsetList\":"+json.dumps(list(ActionQsetList))+"}"

	return HttpResponse(data)


def GetActionPageCount(request):
	page_total = ActionLog.objects.all().count()
	return HttpResponse(page_total)


def GetLoginLogSearchInfo(request):
	try:
		k_words = request.POST.get('k_words','').encode('utf-8')
		s_page = request.POST.get('s_page','')
		page_size = request.POST.get('page_size','')
		GetLoginLogSearchInfo_obj = LoginLog.objects.filter(Q(id__contains=str(k_words)) \
            | Q(Loginuser__contains=str(k_words)) \
            | Q(Logintime__contains=str(k_words)) \
            | Q(Logouttime__contains=str(k_words)) \
            | Q(Logaction__contains=str(k_words)) \
            | Q(LogIP__contains=str(k_words))).values().order_by('-id')[(int(s_page)-1)*int(page_size):int(s_page)*int(page_size)]
		data = "{\"GetLoginLogSearchInfo_obj\":"+json.dumps(list(GetLoginLogSearchInfo_obj))+"}"
		if k_words != "":
			ActionLog.objects.create(Actionuser=request.session['LoginName'],\
        							 Actiontime=time.strftime('%Y-%m-%d %H:%M:%S'),\
        							 Actiontype=u'登录日志查询',\
        							 Actionmodule='-',\
        							 Actioninfo=u'查询内容:'+request.POST.get('k_words',''))
		return HttpResponse(data)
	except Exception as e:
		return HttpResponse(e)

def GetLoginLogSearchCount(request):
    try:
        k_words = request.POST.get('k_words','').encode('utf-8')
        page_total = LoginLog.objects.filter(Q(id__contains=str(k_words)) \
        	| Q(Loginuser__contains=str(k_words)) \
            | Q(Logintime__contains=str(k_words)) \
            | Q(Logouttime__contains=str(k_words)) \
            | Q(Logaction__contains=str(k_words)) \
            | Q(LogIP__contains=str(k_words))).count()
        return HttpResponse(page_total)
    except Exception as e:
        return HttpResponse('303')
