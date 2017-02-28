#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render,HttpResponse,render_to_response
from django.db.models import Q
from usermanage.models import *
from public.publicvar import *
from log.models import ActionLog
from pwd import getpwnam
import json
import time
import os

# Create your views here.
curr_date_str = time.strftime('%Y-%m-%d %H:%M:%S')#获取当前时间字符串

def index(request):
	if 'LoginName' not in request.session:
		return HttpResponseRedirect('/login/')
	return render(request,'usermanage/user.html',{'LoginName': request.session['LoginName'],
												  'navbar':'用户管理',
												  'url':'/usermanage/',
												  'have_publish':'1',
												  'have_review':'1',
												  'have_test':'1'})


def GetUserList(request):
	try:
		s_page = request.POST.get('s_page','')
		page_size = request.POST.get('page_size','')
		# UserInfo_obj = UserInfo.objects.values().order_by('-user')[(int(s_page)-1)*int(page_size):int(s_page)*int(page_size)]
		UserInfo_obj = UserInfo.objects.values().order_by('-user')[(int(s_page)-1)*int(page_size):int(s_page)*int(page_size)]
		data = "{\"UserInfo_obj\":"+json.dumps(list(UserInfo_obj))+"}"
		return HttpResponse(data)
	except Exception as e:
		return HttpResponse('302')

def GetUserListCount(request):
    try:
        #返回模块配置列表总记录数
        page_total = UserInfo.objects.all().count()
        return HttpResponse(page_total)
    except Exception as e:
        return HttpResponse('303')


def GetUserSearchList(request):
    try:
        '''
        返回用户表查询模块配置列表
        '''
        k_words = request.POST.get('k_words','').encode('utf-8')
        # return HttpResponse(k_words)
        s_page = request.POST.get('s_page','')
        # e_page = request.POST.get('e_page','')
        page_size = request.POST.get('page_size','')
        # if request.method  == 'GET':
        # ProjectInfo_obj = Project.objects.values().order_by('-id')[(int(s_page)-1)*int(page_size):int(s_page)*int(page_size)]
        # ProjectInfo_obj = Project.objects.filter(project_name='[ucweb]').values()
        UserInfo_obj = UserInfo.objects.filter(Q(user__contains=str(k_words)) \
            | Q(ftp_path__contains=str(k_words)) \
            | Q(remark__contains=str(k_words))).values().order_by('-user')[(int(s_page)-1)*int(page_size):int(s_page)*int(page_size)]
        data = "{\"UserInfo_obj\":"+json.dumps(list(UserInfo_obj))+"}"
        if k_words != "":
        	ActionLog.objects.create(Actionuser=request.session['LoginName'],\
        							 Actiontime=time.strftime('%Y-%m-%d %H:%M:%S'),\
        							 Actiontype=u'用户数据查询',\
        							 Actionmodule='-',\
        							 Actioninfo=u'查询内容:'+request.POST.get('k_words',''))

        return HttpResponse(data)
    except Exception as e:
        return HttpResponse(e)

def GetUserSearchCount(request):
    try:
        #返回用户表查询模块配置列表总记录数
        k_words = request.POST.get('k_words','').encode('utf-8')
        # return HttpResponse(k_words)
        page_total = UserInfo.objects.filter(Q(user__contains=str(k_words)) \
            | Q(ftp_path__contains=str(k_words)) \
            | Q(remark__contains=str(k_words))).count()
        return HttpResponse(page_total)
    except Exception as e:
        return HttpResponse('303')


def UserAdd(request):
	'''
	判断/home/ftp/用户 这个文件夹是否存在，不存在则创建，赋予系统执行者的属组权限
	'''
	username = request.POST.get('username','')
	userpasswd = request.POST.get('userpasswd','')
	have_publish = request.POST.get('have_publish','')
	have_review = request.POST.get('have_review','')
	have_test = request.POST.get('have_test','')
	remark = request.POST.get('remark','')
	try:
		UserBasePath = '/home/ftp/'
		NewFileDir = UserBasePath+username
		if os.path.exists(NewFileDir):
			if os.path.isdir(NewFileDir):
				return HttpResponse('FileExist')
			elif os.path.isfile(NewFileDir):
				os.makedirs(NewFileDir)
				os.chown(NewFileDir,getpwnam(System_Excute_User)[2],getpwnam(System_Excute_User).pw_uid)
			else:return HttpResponse('UnkonwnError')
		else:

			os.makedirs(NewFileDir)
			# return HttpResponse('1111')
			os.chown(NewFileDir,getpwnam(System_Excute_User)[2],getpwnam(System_Excute_User).pw_uid)
		UserInfo.objects.create(user=username,
								password=userpasswd,
								ftp_path='/home/ftp/'+username,
								remark=remark,
								have_publish=have_publish,
								have_review=have_review,
								have_test=have_test,
								create_time=time.strftime('%Y-%m-%d %H:%M:%S'),
								user_status='1')
		ActionLog.objects.create(Actionuser=request.session['LoginName'],
								 Actiontime=time.strftime('%Y-%m-%d %H:%M:%S'),
								 Actiontype=u'新增用户',
								 Actionmodule='usermanage',
								 Actioninfo=u'用户名:'+username+u';发布权限:'+have_publish+u';审核权限:'+have_review+u';测试权限:'+have_publish+u';用户备注:'+remark)
		return HttpResponse('success')
	except Exception as e:
		return HttpResponse(e)



def UserCheck(request):
	username = request.POST.get('username','')
	user_is_exist = UserInfo.objects.filter(user=username).count()
	return HttpResponse(user_is_exist)


def UserStatusSwitch(request):
	username = request.POST.get('username','')
	status = request.POST.get('status','')
	try:
		UserInfo.objects.filter(user=username).update(user_status=status,update_time=time.strftime('%Y-%m-%d %H:%M:%S'),update_user=request.session['LoginName'])
		ActionLog.objects.create(Actionuser=request.session['LoginName'],
								 Actiontime=time.strftime('%Y-%m-%d %H:%M:%S'),
								 Actiontype=u'更改用户状态',
								 Actionmodule='usermanage',
								 Actioninfo=u'用户名:'+username+u';更改后用户状态为:'+status+u';(0-禁用用户；1-启用用户)')

		return HttpResponse('Switched')
	except Exception as e:
		return HttpResponse('MissSwitched')

