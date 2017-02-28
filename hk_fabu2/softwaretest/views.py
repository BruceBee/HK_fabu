# -*- coding:utf-8 -*-
from django.shortcuts import render,HttpResponse, render_to_response
from django.db.models import Q
from review.models import ForReview,ReviewAction
from softwaretest.models import SoftwareTest
from log.models import ActionLog
from public.publicfunction import *

import json
import time

curr_date_str = time.strftime('%Y-%m-%d %H:%M:%S')#获取当前时间字符串


# Create your views here.

#测试模块首页
def index(request):
	ForReview_total = ForReview.objects.all().count()
	# ForReview_total = ForReview.objects.filter(is_active='0').count()
	# ForTest_total = ReviewAction.objects.filter(publish_status='审核通过,已发布').count()
	ForTest_total = SoftwareTest.objects.filter(test_status='0').count()
	ForTest_success = SoftwareTest.objects.filter(test_status='1').count()
	ForTest_fail = SoftwareTest.objects.filter(test_status='2').count()

	PublishSuccess_total = int(ForTest_total)+int(ForTest_success)+int(ForTest_fail)

	if ForReview_total == 0:
		PublishSuccess_percent = 0
	else:
		PublishSuccess_percent = ("%.f" %(float(PublishSuccess_total)/float(ForReview_total)*100))
	if ForTest_success+ForTest_fail == 0:
		TestSuccess_percent =0
	else:
		TestSuccess_percent = ("%.f" %(float(ForTest_success)/(float(ForTest_success) + float(ForTest_fail))*100))

	have_publish,have_review,have_test = GetUserAuth(request.session['LoginName'])
	return render(request,'softwaretest/TestReview.html',{'LoginName': request.session['LoginName'],
														  'ForReview_total':ForReview_total,
														  'PublishSuccess_total':PublishSuccess_total,
														  'PublishSuccess_percent':PublishSuccess_percent,
														  'ForTest_total':ForTest_total,
														  'ForTest_success':ForTest_success,
														  'ForTest_fail':ForTest_fail,
														  'TestSuccess_percent':TestSuccess_percent,
														  'navbar':'系统测试',
														  'url':'/softwaretest/',
														  'have_publish':have_publish,
														  'have_review':have_review,
														  'have_test':have_test})


def LastTestInfo(request):
	SoftwareTest_obj = SoftwareTest.objects.all().values()
	LastTestId = SoftwareTest.objects.values().order_by('-id')[0]['publish_id']
	# SoftwareTest_obj = SoftwareTest.objects.all().values().order_by('-id')[0]
	LastSoftwareTest = ReviewAction.objects.filter(publish_id=LastTestId).values()
	data = "{\"LastSoftwareTest\":"+json.dumps(list(LastSoftwareTest))+"}"
	return HttpResponse(data)

#查询待测试数据
def SoftwareTestPageSearchCount(request):
	#查询待测试列表数量
    try:
        k_words = request.POST.get('k_words','').encode('utf-8')
        page_total = SoftwareTest.objects.filter(test_status='0').filter(Q(publish_id__contains=str(k_words)) \
            | Q(publish_type__contains=str(k_words)) \
            | Q(publish_user__contains=str(k_words)) \
            | Q(publish_module__contains=str(k_words)) \
            | Q(publish_status__contains=str(k_words)) \
            | Q(create_time__contains=str(k_words)) \
            | Q(publish_serverlist__contains=str(k_words)) \
            | Q(review_time__contains=str(k_words)) \
            | Q(review_info__contains=str(k_words))).count()
        return HttpResponse(page_total)
    except Exception as e:
        return HttpResponse('303')
	# page_total = SoftwareTest.objects.filter(test_status='0').count()
	# return HttpResponse(page_total)	


def SoftwareTestSearchList(request):
	#查询待测试列表
    try:
        k_words = request.POST.get('k_words','').encode('utf-8')
        s_page = request.POST.get('s_page','')
        page_size = request.POST.get('page_size','')
        SoftwareTest_obj = SoftwareTest.objects.filter(test_status='0').filter(Q(publish_id__contains=str(k_words)) \
            | Q(publish_type__contains=str(k_words)) \
            | Q(publish_user__contains=str(k_words)) \
            | Q(publish_module__contains=str(k_words)) \
            | Q(publish_status__contains=str(k_words)) \
            | Q(create_time__contains=str(k_words)) \
            | Q(publish_serverlist__contains=str(k_words)) \
            | Q(review_time__contains=str(k_words)) \
            | Q(review_info__contains=str(k_words))).values().order_by('-publish_id')[(int(s_page)-1)*int(page_size):int(s_page)*int(page_size)]
        data = "{\"SoftwareTest_obj\":"+json.dumps(list(SoftwareTest_obj))+"}"
        if k_words != "":
        	ActionLog.objects.create(Actionuser=request.session['LoginName'],\
        							 Actiontime=time.strftime('%Y-%m-%d %H:%M:%S'),\
        							 Actiontype=u'待测试数据查询',\
        							 Actionmodule='-',\
        							 Actioninfo=u'查询内容:'+request.POST.get('k_words',''))
        return HttpResponse(data)
    except Exception as e:
        return HttpResponse(e)

	# s_page = request.POST.get('s_page','')
	# page_size = request.POST.get('page_size','')
	# TestQsetList = SoftwareTest.objects.filter(test_status='0').values().order_by('-id')[(int(s_page)-1)*int(page_size):int(s_page)*int(page_size)]
	# data = "{\"TestQsetList\":"+json.dumps(list(TestQsetList))+"}"
	
	# return HttpResponse(data)


#获取待测试数据
def SoftwareTestPageCount(request):
	#获取id列表（状态为待测试）
	page_total = SoftwareTest.objects.filter(test_status='0').count()
	return HttpResponse(page_total)	

def SoftwareTestList(request):
	'''
	返回待测试列表
	'''
	s_page = request.POST.get('s_page','')
	# e_page = request.POST.get('e_page','')
	page_size = request.POST.get('page_size','')
	# if request.method  == 'GET':
	'''
	TestIdList =[]
	TestQsetList=[]
	for i in SoftwareTest.objects.filter(test_status='0'):
		TestQsetList.append(i.publish_id)
		Test_obj = ReviewAction.objects.get(publish_id=i.publish_id)
		SoftwareTest.objects.update()
	data = "{\"TestQsetList\":"+json.dumps(list(TestQsetList))+"}"
	'''

	TestQsetList = SoftwareTest.objects.filter(test_status='0').values().order_by('-id')[(int(s_page)-1)*int(page_size):int(s_page)*int(page_size)]
	data = "{\"TestQsetList\":"+json.dumps(list(TestQsetList))+"}"


	# review_obj = ForReview.objects.filter(review_owner=request.session['LoginName']).values().order_by('-id')[(int(s_page)-1)*int(page_size):int(s_page)*int(page_size)]
	# data = "{\"review_data\":"+json.dumps(list(review_obj))+"}"
	
	return HttpResponse(data)
	# else:
		# pass	

#获取测试处理界面
def TestHandle(request,id):
	TestHandleData = SoftwareTest.objects.get(publish_id=id)
	have_publish,have_review,have_test = GetUserAuth(request.session['LoginName'])
	return render(request,'softwaretest/TestHandle.html',{'publish_id':TestHandleData.publish_id,
														  'publish_type':TestHandleData.publish_type,
														  'publish_user':TestHandleData.publish_user,
														  'publish_status':TestHandleData.publish_status,
														  'publish_module':TestHandleData.publish_module,
														  'publish_filename':TestHandleData.publish_filename,
														  'file_uploadtime':TestHandleData.file_uploadtime,
														  'create_time':TestHandleData.create_time,
														  'publish_serverlist':TestHandleData.publish_serverlist,
														  'publish_detail':TestHandleData.publish_detail,
														  'review_owner':TestHandleData.review_owner,
														  'review_time':TestHandleData.review_time,
														  'review_info':TestHandleData.review_info,
														  'publish_strtime':TestHandleData.publish_strtime,
														  'publish_endtime':TestHandleData.publish_endtime,
														  'LoginName': request.session['LoginName'],
														  'navbar':'系统测试',
														  'url':'/softwaretest/',
														  'have_publish':have_publish,
														  'have_review':have_review,
														  'have_test':have_test})

#获取最近十条发布申请数据
def GetLastTenPublishInfo(request):
	TenPublishInfo = ForReview.objects.values('publish_user','create_time','id','publish_module').order_by('-create_time')[:10]
	data = "{\"TenPublishInfo\":"+json.dumps(list(TenPublishInfo))+"}"
	return HttpResponse(data)
#获取最近十条审核发布数据
def GetLastTenTestInfo(request):
	TenTestInfo = ReviewAction.objects.values('review_owner','review_time','publish_id','publish_status','publish_module').order_by('-review_time')[:10]

	data = "{\"TenTestInfo\":"+json.dumps(list(TenTestInfo))+"}"
	return HttpResponse(data)

#处理测试
def EndTest(request):
	'''
	获取当前ID，获取当前的测试意见,更新后台数据
	'''
	test_info = request.POST["test_info"]
	test_action = request.POST["test_action"]
	test_id = request.POST["test_id"]

	# return HttpResponse(test_id)
	SoftwareTest.objects.filter(publish_id=test_id).update(test_user=request.session['LoginName'],\
		test_starttime=time.strftime('%Y-%m-%d %H:%M:%S'),\
		test_endtime=time.strftime('%Y-%m-%d %H:%M:%S'),\
		test_detail=test_info,
		test_status=test_action)


	ReportObj = SoftwareTest.objects.get(publish_id=test_id)
	#记录测试操作日志
	ActionLog.objects.create(Actionuser=request.session['LoginName'],Actiontime=ReportObj.test_starttime,\
		Actiontype=u'系统测试',Actionmodule=ReportObj.publish_module,\
		Actioninfo=u'发布ID:'+ReportObj.publish_id+u';系统测试意见:'+test_action+u';【0:待测试;1:测试完成，通过;2:测试完成，不通过;3:其他】')

	# ReportObj = SoftwareTest.objects.get(publish_id=test_id)
	have_publish,have_review,have_test = GetUserAuth(request.session['LoginName'])
	return render(request,'softwaretest/TestReport.html',{'publish_id':ReportObj.publish_id,
														  'publish_type':ReportObj.publish_type,
														  'publish_user':ReportObj.publish_user,
														  'publish_status':ReportObj.publish_status,
														  'publish_module':ReportObj.publish_module,
														  'publish_filename':ReportObj.publish_filename,
														  'file_uploadtime':ReportObj.file_uploadtime,
														  'create_time':ReportObj.create_time,
														  'publish_serverlist':ReportObj.publish_serverlist,
														  'publish_detail':ReportObj.publish_detail,
														  'review_owner':ReportObj.review_owner,
														  'review_time':ReportObj.review_time,
														  'review_info':ReportObj.review_info,
														  'publish_strtime':ReportObj.publish_strtime,
														  'publish_endtime':ReportObj.publish_endtime,
														  'test_user':ReportObj.test_user,
														  'test_starttime':ReportObj.test_starttime,
														  'test_endtime':ReportObj.test_endtime,
														  'test_detail':ReportObj.test_detail,
														  'test_status':ReportObj.test_status,
														  'LoginName': request.session['LoginName'],
														  'navbar':'系统测试',
														  'url':'/softwaretest/',
														  'have_publish':have_publish,
														  'have_review':have_review,
														  'have_test':have_test})

#查看测试报告
def TestReport(request,id):

	ReportObj = SoftwareTest.objects.get(publish_id=id)
	have_publish,have_review,have_test = GetUserAuth(request.session['LoginName'])
	return render(request,'softwaretest/TestReport.html',{'publish_id':ReportObj.publish_id,
														  'publish_type':ReportObj.publish_type,
														  'publish_user':ReportObj.publish_user,
														  'publish_status':ReportObj.publish_status,
														  'publish_module':ReportObj.publish_module,
														  'publish_filename':ReportObj.publish_filename,
														  'file_uploadtime':ReportObj.file_uploadtime,
														  'create_time':ReportObj.create_time,
														  'publish_serverlist':ReportObj.publish_serverlist,
														  'publish_detail':ReportObj.publish_detail,
														  'review_owner':ReportObj.review_owner,
														  'review_time':ReportObj.review_time,
														  'review_info':ReportObj.review_info,
														  'test_user':ReportObj.test_user,
														  'test_starttime':ReportObj.test_starttime,
														  'test_endtime':ReportObj.test_endtime,
														  'test_detail':ReportObj.test_detail,
														  'test_status':ReportObj.test_status,
														  'LoginName': request.session['LoginName'],
														  'navbar':'系统测试',
														  'url':'/softwaretest/',
														  'have_publish':have_publish,
														  'have_review':have_review,
														  'have_test':have_test})


#查询已测试数据
def GetActionSearchListPageCount(request):
    try:
    	Test_statue = request.POST.get('args','')
        k_words = request.POST.get('k_words','').encode('utf-8')
        page_total = SoftwareTest.objects.filter(test_status=Test_statue).filter(Q(publish_id__contains=str(k_words)) \
            | Q(publish_type__contains=str(k_words)) \
            | Q(publish_user__contains=str(k_words)) \
            | Q(publish_module__contains=str(k_words)) \
            | Q(publish_status__contains=str(k_words)) \
            | Q(create_time__contains=str(k_words)) \
            | Q(publish_serverlist__contains=str(k_words)) \
            | Q(review_owner__contains=str(k_words)) \
            | Q(review_time__contains=str(k_words)) \
            | Q(review_info__contains=str(k_words)) \
            | Q(test_user__contains=str(k_words)) \
            | Q(test_starttime__contains=str(k_words))).count()
        return HttpResponse(page_total)
    except Exception as e:
        return HttpResponse('303')
	# Test_statue = request.POST.get('args','')
	# action_total = SoftwareTest.objects.filter(test_status=Test_statue).count()

	# return HttpResponse(action_total)

def GetActionSearchList(request):
    try:
    	Test_statue = request.POST.get('args','')
        k_words = request.POST.get('k_words','').encode('utf-8')
        s_page = request.POST.get('s_page','')
        page_size = request.POST.get('page_size','')
        GetActionData = SoftwareTest.objects.filter(test_status=Test_statue).filter(Q(publish_id__contains=str(k_words)) \
            | Q(publish_type__contains=str(k_words)) \
            | Q(publish_user__contains=str(k_words)) \
            | Q(publish_module__contains=str(k_words)) \
            | Q(publish_status__contains=str(k_words)) \
            | Q(create_time__contains=str(k_words)) \
            | Q(publish_serverlist__contains=str(k_words)) \
            | Q(review_owner__contains=str(k_words)) \
            | Q(review_time__contains=str(k_words)) \
            | Q(review_info__contains=str(k_words)) \
            | Q(test_user__contains=str(k_words)) \
            | Q(test_starttime__contains=str(k_words))).values().order_by('-id')[(int(s_page)-1)*int(page_size):int(s_page)*int(page_size)]
        data = "{\"GetActionData\":"+json.dumps(list(GetActionData))+"}"
        if k_words != "":
        	ActionLog.objects.create(Actionuser=request.session['LoginName'],\
        							 Actiontime=time.strftime('%Y-%m-%d %H:%M:%S'),\
        							 Actiontype=u'已测试数据查询',\
        							 Actionmodule='-',\
        							 Actioninfo=u'查询内容:'+request.POST.get('k_words','')+u';查询数据状态:'+Test_statue+u';【0:待测试;1:测试完成，通过;2:测试完成，不通过;3:其他】')

        return HttpResponse(data)
    except Exception as e:
        return HttpResponse(e)
	# Test_statue = request.POST.get('args','')
	# s_page = request.POST.get('s_page','')
	# page_size = request.POST.get('page_size','')
	# TestActionData = SoftwareTest.objects.filter(test_status=Test_statue).values().order_by('-id')[(int(s_page)-1)*int(page_size):int(s_page)*int(page_size)]
	# data = "{\"GetActionData\":"+json.dumps(list(GetActionData))+"}"
	# return HttpResponse(data)

#获取已测试数据
def GetActionListPageCount(request):
	Test_statue = request.POST.get('args','')
	action_total = SoftwareTest.objects.filter(test_status=Test_statue).count()

	return HttpResponse(action_total)

def GetActionList(request):
	Test_statue = request.POST.get('args','')
	s_page = request.POST.get('s_page','')
	page_size = request.POST.get('page_size','')
	TestActionData = SoftwareTest.objects.filter(test_status=Test_statue).values().order_by('-id')[(int(s_page)-1)*int(page_size):int(s_page)*int(page_size)]
	data = "{\"TestActionData\":"+json.dumps(list(TestActionData))+"}"
	return HttpResponse(data)


def Last(request):
	return render(request,'404.html')