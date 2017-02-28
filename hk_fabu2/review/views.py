# -*- coding:utf-8 -*-
from django.shortcuts import render,HttpResponse, render_to_response
from django.db.models import Q
# Create your views here.
import os,commands,re
import json
import time
from review.models import ForReview,ReviewAction
from softwaretest.models import SoftwareTest
from log.models import ActionLog
from review import bulid_report
from index.views import runplaybook
from usermanage.models import UserInfo
from public.publicvar import *
from public.publicfunction import *
from index.models import UserLoginInfo, Logging
from projectinfo.models import Project

import HTMLParser
html_parser = HTMLParser.HTMLParser()

curr_date_str = time.strftime('%Y-%m-%d %H:%M:%S')#获取当前时间字符串
cmd = '/usr/bin/ansible-playbook %s --extra-vars "project_name=%s project_pack=%s project_port=%s backup_time=%s" -f %d -v'


#html转义
def replace_html(s):
    s = s.replace('&quot;','"')
    s = s.replace('&amp;','&')
    s = s.replace('&lt;','<')
    s = s.replace('&gt;','>')
    s = s.replace('&nbsp;',' ')
    # s = s.replace(' - 361way.com','')
    # print s
    return s

def runplaybook(yml_path, project_pack, project_name, project_port, backup_time, num):
    """
    运行ansible-playbook命令
    :param yml_path: playbook脚本(yml文件)路径
    :param project_pack: 压缩包路径
    :param project_name: 项目名
    :param backup_time: 备份文件文件名中的时间
    :param num: 线程数量==项目服务器数量
    :return: 运行状态, output输出
    """
    status, output = commands.getstatusoutput(cmd % (yml_path, project_name, project_pack, project_port, backup_time, num))
#    status, output = commands.getstatusoutput(cmd % (yml_path, project_name, project_pack, project_port, backup_time, 1))
    return status, output

def review(request):
	'''
	主review函数
	'''
	have_publish,have_review,have_test = GetUserAuth(request.session['LoginName'])
	return render(request,'review/review.html',{'LoginName': request.session['LoginName'],
										 'navbar':'发布审核',
										 'url':'/review/',
										 'have_publish':have_publish,
										 'have_review':have_review,
										 'have_test':have_test})


def review_handle(request,id):
	'''
	js请求函数，获取js所选请求的详细，进入待审界面
	'''


	review_obj = ForReview.objects.get(id=id)
	#禁止提交审核给自己
	
	if request.session['LoginName'] == review_obj.publish_user:
		is_editable = "False"
	else:
		is_editable = "True"
	publish_detail = html_parser.unescape(review_obj.publish_detail)

	# return HttpResponse(publish_detail)
	# return HttpResponse(review_obj.publish_detail)
	have_publish,have_review,have_test = GetUserAuth(request.session['LoginName'])
	return render(request,'review/review_handle.html',{'publish_id':review_obj.id,\
												'publish_type':review_obj.publish_type,\
												'publish_user':review_obj.publish_user,\
												'publish_status':review_obj.publish_status,\
												'publish_module':review_obj.publish_module,\
												'publish_filename':review_obj.publish_filename,\
												'create_time':review_obj.create_time,\
												'publish_serverlist':review_obj.publish_serverlist,\
												'publish_detail':review_obj.publish_detail,\
												'is_editable':is_editable,\
												'LoginName': request.session['LoginName'],
												'navbar':'发布审核',
												'url':'/review/',
												'have_publish':have_publish,
												'have_review':have_review,
												'have_test':have_test})

def result(request):
	return render(request, 'review/result.html', {'RunPlaybookState': 'Done',\
        	'output_list':'这是一个正确的返回值',\
        	'LoginName': request.session['LoginName'],\
        	'status':'0',\
        	'publish_id':'123'})



def review_publish(request):
	have_publish,have_review,have_test = GetUserAuth(request.session['LoginName'])
	'''
	发布审核函数
	0-审核通过，正式发布
	1-审核不通过，不予发布
	'''
	if request.method == 'POST':
		publish_id = request.POST['publish_id']
		review_action = request.POST['publish_action'].split('-')[0]
		# return HttpResponse(review_action)
		review_info = request.POST['review_info']
		review_obj = ForReview.objects.filter(id=publish_id)

		for i in review_obj:
			publish_type =i.publish_type
			publish_user =i.publish_user
			publish_module =i.publish_module
			publish_filename =i.publish_filename
			file_uploadtime =i.file_uploadtime
			create_time =i.create_time
			publish_serverlist =i.publish_serverlist
			publish_detail =i.publish_detail

		if review_action == '0':
			publish_status='审核通过,已发布'
		else:
			publish_status='审核不通过,禁止发布'


		review_dict ={
		'publish_id':publish_id,
		'publish_status':publish_status,
		'publish_type':publish_type,
		'publish_module':publish_module,
		'publish_filename':publish_filename,
		'file_uploadtime':file_uploadtime,
		'publish_user':publish_user,
		'create_time':create_time,
		'publish_detail':publish_detail,
		'publish_serverlist':publish_serverlist,
		'review_owner':request.session['LoginName'],
		'review_time':time.strftime('%Y-%m-%d %H:%M:%S'),
		'review_info':review_info,
		}

		#ReviewAction表里的review_time为审批提交时间，也是部署开始时间

		ReviewAction.objects.create(**review_dict)
		#ForReview表对应数据设置不活跃
		review_obj.update(is_active='1',update_user=request.session['LoginName'])
		#记录审批操作日志
		ActionLog.objects.create(Actionuser=request.session['LoginName'],Actiontime=review_dict['review_time'],\
			Actiontype=u'发布审批',Actionmodule=review_dict['publish_module'],\
			Actioninfo=u'发布ID:'+review_dict['publish_id']+u';发布审批意见:'+review_action+u';【0-审核通过,已发布;1-审核不通过,禁止发布;】')

		runplaybook_state = 'Done'      # runplaybook状态初始化为Done

		# project_pack = os.path.join('/home/ftp/admin/', publish_filename)

		# if publish_user == 'admin':
		# 	project_pack = os.path.join('/home/ftp/admin/', publish_filename)
		# else:
		# 	project_pack = os.path.join('/home/ftp/'+publish_user[:4]+publish_user[-2:]+'/', publish_filename)
		project_pack = os.path.join('/home/ftp/'+publish_user+'/', publish_filename)


		(the_yml_path, str_fabu) = (newfabu_yml_path, '(全新部署)') if 'newfabu' in request.POST else (fabu_yml_path, '(增量部署)')    # 判断是否为全新发布

		if review_action == '0':
			publish_strtime = time.strftime('%Y-%m-%d %H:%M:%S')
			#正式发布
			status, output = runplaybook(the_yml_path, project_pack, publish_module, the_ssh_port, publish_strtime, len(publish_serverlist))
			publish_endtime = time.strftime('%Y-%m-%d %H:%M:%S')

			output_list = output.split('\n')
			
			if status != 0:
				RunPlaybookOutput = 'FAILD'
				ActionLog.objects.create(Actionuser=request.session['LoginName'],Actiontime=publish_strtime,\
						Actiontype=u'审批后发布',Actionmodule=publish_module,\
						Actioninfo=u'发布ID:'+publish_id+u';发布失败！！！'+u';开始时间:'+publish_strtime+u';结束时间:'+publish_endtime)
				return render(request,'review/result.html', {'RunPlaybookState': RunPlaybookOutput,
														  'output_list':output_list,
														  'LoginName': request.session['LoginName'],
														  'status':status,
														  'publish_id':publish_id,
														  'navbar':'发布结果',
														  'url':'/review/',
														  'have_publish':have_publish,
														  'have_review':have_review,
														  'have_test':have_test})

			RunPlaybookOutput = ""      # 输出到前端页面的运行状态信息
			for i, value in enumerate(output_list):# 检测失败信息
				if value.strip().startswith('fatal:'):
					RunPlaybookOutput+=value
					runplaybook_state = 'False'# 出现失败信息则将runplaybook运行状态变更为False
					#发布失败，记录操作动作
					ActionLog.objects.create(Actionuser=request.session['LoginName'],Actiontime=publish_strtime,\
						Actiontype=u'审批后发布',Actionmodule=publish_module,\
						Actioninfo=u'发布ID:'+publish_id+u';发布失败！！！'+u';开始时间:'+publish_strtime+u';结束时间:'+publish_endtime)
					return render(request,'review/result.html', {'RunPlaybookState': RunPlaybookOutput,
														  'output_list':output_list,
														  'LoginName': request.session['LoginName'],
														  'status':status,
														  'publish_id':publish_id,
														  'navbar':'发布结果',
														  'url':'/review/',
														  'have_publish':have_publish,
														  'have_review':have_review,
														  'have_test':have_test})
			if len(RunPlaybookOutput) == 0:
				RunPlaybookOutput+=runplaybook_state
				output_list = 'PLAY RECAP'+output.split('PLAY RECAP')[1]
				SoftwareTest.objects.create(publish_id=publish_id,\
					publish_status='审核通过,已发布',\
	            	publish_type=publish_type,\
	            	publish_module=publish_module,\
	            	publish_filename=publish_filename,\
	            	file_uploadtime=file_uploadtime,\
	            	publish_user=publish_user,\
	            	create_time=create_time,\
	            	publish_detail=publish_detail,\
	            	publish_serverlist=publish_serverlist,\
	            	publish_strtime=publish_strtime,\
	            	publish_endtime=publish_endtime,\
	            	review_owner=request.session['LoginName'],\
	            	review_time=review_dict['review_time'],\
	            	review_info=review_info,)
				#SoftwareTest表里的review_time为部署结束时间
				#发布成功，记录操作动作
				ActionLog.objects.create(Actionuser=request.session['LoginName'],Actiontime=publish_strtime,\
						Actiontype=u'审批后发布',Actionmodule=publish_module,\
						Actioninfo=u'发布ID:'+publish_id+u';发布成功'+u';开始时间:'+publish_strtime+u';结束时间:'+publish_endtime)
				return render(request,'review/result.html', {'RunPlaybookState': RunPlaybookOutput,
													  'output_list':output_list,
													  'LoginName': request.session['LoginName'],
													  'status':status,
													  'publish_id':publish_id,
													  'navbar':'发布结果',
													  'url':'/review/',
													  'have_publish':have_publish,
													  'have_review':have_review,
													  'have_test':have_test})

		else:
			# return HttpResponse('您是取消发布')
			review_cancle = ReviewAction.objects.get(publish_id=publish_id)
			return render(request,'review/publish_report.html',{'publish_id':review_cancle.publish_id,
														 'publish_type':review_cancle.publish_type,
														 'publish_user':review_cancle.publish_user,
														 'publish_status':review_cancle.publish_status,
														 'publish_module':review_cancle.publish_module,
														 'publish_filename':review_cancle.publish_filename,
														 'create_time':review_cancle.create_time,
														 'publish_serverlist':review_cancle.publish_serverlist,
														 'publish_detail':review_cancle.publish_detail,
														 'review_owner':review_cancle.review_owner,
														 'review_time':review_cancle.review_time,
														 'review_info':review_cancle.review_info,
														 'LoginName': request.session['LoginName'],
														 'navbar':'发布审核',
														 'url':'/review/',
														 'have_publish':have_publish,
														 'have_review':have_review,
														 'have_test':have_test})


def publish_report(request,id):
	'''
	界面返回完整web发布报告
	'''
	review_obj = ReviewAction.objects.get(publish_id=id)
	have_publish,have_review,have_test = GetUserAuth(request.session['LoginName'])
	return render(request,'review/publish_report.html',{'publish_id':review_obj.publish_id,
												 'publish_type':review_obj.publish_type,
												 'publish_user':review_obj.publish_user,
												 'publish_status':review_obj.publish_status,
												 'publish_module':review_obj.publish_module,
												 'publish_filename':review_obj.publish_filename,
												 'create_time':review_obj.create_time,
												 'publish_serverlist':review_obj.publish_serverlist,
												 'publish_detail':review_obj.publish_detail,
												 'review_owner':review_obj.review_owner,
												 'review_time':review_obj.review_time,
												 'review_info':review_obj.review_info,
												 'LoginName': request.session['LoginName'],
												 'navbar':'发布审核',
												 'url':'/review/',
												 'have_publish':have_publish,
												 'have_review':have_review,
												 'have_test':have_test})


def publish_cancle(request):

	publish_id = request.POST.get('publish_id')
	try:
		ForReview.objects.filter(id=publish_id).update(is_active='1')
		CanclePublish = ForReview.objects.get(id=publish_id)
		#记录操作日志
		ActionLog.objects.create(Actionuser=request.session['LoginName'],Actiontime=time.strftime('%Y-%m-%d %H:%M:%S'),Actiontype=u'取消发布申请',Actionmodule=CanclePublish.publish_module,Actioninfo=u'发布ID:'+publish_id)
		return HttpResponse('1')
	except Exception as e:
		return HttpResponse('id is not exist')

def testDownload(request):
	ret = bulid_report.bulid_docs("1")
	return HttpResponse(ret)	


def DownloadReport(request):
	'''
	调用bulid_report函数生成docx
	'''

	downloadID = request.POST.get('downloadID')
	downloadtype = request.POST.get('downloadtype')

	downloadObject = SoftwareTest.objects.get(publish_id=downloadID)


	'''
	downloadtype:
	1:word
	2:excel
	'''

	#发布部分项与值
	base_itemlist = [u'软件系统名称',u'系统版本号',u'发布类型:',u'发布状态',u'发布ID',u'版本发布者',\
	u'发布模块名',u'发布文件名',u'申请时间',u'发布主机',u'发布详情']

	base_valuelist = [u'华康web3.0','3.0.1',downloadObject.publish_type,downloadObject.publish_status,\
	downloadObject.publish_id,downloadObject.publish_user,downloadObject.publish_module,downloadObject.publish_filename,\
	downloadObject.create_time,downloadObject.publish_serverlist,u'见sheet2']


	#审批部分项与值
	review_itemlist = [u'审批人',u'审批/发布时间',u'审批意见']
	review_valuelist = [downloadObject.review_owner,downloadObject.review_time,downloadObject.review_info]


	#测试部分项与值
	test_itemlist = [u'测试状态',u'测试人员',u'测试时间',u'测试意见']
	test_valuelist = [downloadObject.test_status+u'【意见说明：0:待测试；1:测试完成，通过；2:测试完成，不通过；3:其他】',downloadObject.test_user,downloadObject.test_endtime,u'见sheet3']


	
	if downloadtype == '1':
		ret = bulid_report.bulid_docs(downloadID,base_itemlist,base_valuelist,review_itemlist,review_valuelist,test_itemlist,test_valuelist,downloadObject.publish_detail,downloadObject.test_detail)
	else:
		ret = bulid_report.bulid_excel(downloadID,base_itemlist,base_valuelist,review_itemlist,review_valuelist,test_itemlist,test_valuelist,downloadObject.publish_detail,downloadObject.test_detail)
	return HttpResponse(ret)


def Downloadaction(request,offset):
	'''
    offset='doc201612201111'
    the_file_name是带后缀的完整文件名称
    '''
	from django.http import StreamingHttpResponse
	def file_iterator(file_name,chunk_size=512):
		with open(file_name) as f:
			while True:
				c = f.read(chunk_size)
				if c:
					yield c
				else:
					break

	the_file_name = offset[3:]+'.'+offset[0:3]
	response = StreamingHttpResponse(file_iterator('/home/fabu/hk_fabu2/review/download/'+offset[0:3]+'/'+offset[3:]+'.'+offset[0:3]))
	response['Content-Type'] = 'application/octet-stream'
	response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)
	return response


def GetPublishlistPageCount(request):
	#返回发布申请列表总记录数
	page_total = ForReview.objects.filter(publish_user=request.session['LoginName'],is_active='0').count()
	return HttpResponse(page_total)	

def GetPublishlist(request):
	'''
	获取由用户自己发起的发布申请
	'''
	s_page = request.POST.get('s_page','')
	# e_page = request.POST.get('e_page','')
	page_size = request.POST.get('page_size','')
	# if request.method == 'GET':
	review_obj = ForReview.objects.filter(publish_user=request.session['LoginName'],is_active='0').values().order_by('-id')[(int(s_page)-1)*int(page_size):int(s_page)*int(page_size)]
	page_total = ForReview.objects.filter(publish_user=request.session['LoginName'],is_active='0').count()

	data = "{\"review_data\":"+json.dumps(list(review_obj))+",\"page_total\":"+str(page_total)+"}"
	# data = "{\"review_data\":"+json.dumps(list(review_obj))+"}"
	# data="{\"rows\":"+json.dumps(list(domain_data))+",\"total\":\""+str(total)+"\",\"record_line\":"+json.dumps(list(record_line))+",\"record_type\":"+json.dumps(list(record_type))+"}"
	return HttpResponse(data)
	# else:
	# 	pass			



def PreViewListPageCount(request):
	#返回待审列表总记录数,审批人是‘我’并且活跃状态
	page_total = ForReview.objects.filter(review_owner=request.session['LoginName'],is_active='0').count()
	return HttpResponse(page_total)	


def PreViewList(request):
	'''
	返回待审列表,审批人是‘我’并且活跃状态
	'''
	s_page = request.POST.get('s_page','')
	# e_page = request.POST.get('e_page','')
	page_size = request.POST.get('page_size','')
	# if request.method  == 'GET':
	review_obj = ForReview.objects.filter(review_owner=request.session['LoginName'],is_active='0').values().order_by('-id')[(int(s_page)-1)*int(page_size):int(s_page)*int(page_size)]
	data = "{\"review_data\":"+json.dumps(list(review_obj))+"}"
	return HttpResponse(data)
	# else:
		# pass	



def ReviewActionListPageCount(request):
	#返回审核列表总记录数
	review_statue = request.POST.get('args','')
	if review_statue == '0':
		publish_status = '审核通过,已发布'
	else:
		publish_status = '审核不通过,禁止发布'
	page_total = ReviewAction.objects.filter(Q(publish_status=publish_status),Q(publish_user=request.session['LoginName']) | Q(review_owner=request.session['LoginName'])).count()
	return HttpResponse(page_total)


def ReviewActionList(request):
	'''
	返回已审列表
	'''
	s_page = request.POST.get('s_page','')
	# e_page = request.POST.get('e_page','')
	page_size = request.POST.get('page_size','')
	if request.method == 'GET':

		review_obj = ReviewAction.objects.filter(Q(publish_user=request.session['LoginName']) | Q(review_owner=request.session['LoginName']))
		data = "{\"review_data\":"+json.dumps(list(review_obj))+"}"
		return HttpResponse(data)
	else:
		#返回:通过/不通过，且发布者或审批者为当前登录用户的数据
		review_statue = request.POST.get('args','')
		if review_statue == '0':
			publish_status = '审核通过,已发布'
		else:
			publish_status = '审核不通过,禁止发布'

		review_obj = ReviewAction.objects.filter(Q(publish_status=publish_status),Q(publish_user=request.session['LoginName']) | Q(review_owner=request.session['LoginName'])).values().order_by('-id')[(int(s_page)-1)*int(page_size):int(s_page)*int(page_size)]	
		data = "{\"review_data\":"+json.dumps(list(review_obj))+",\"page_total\":\""+str(review_obj.count())+"\"}"
		# data = "{\"review_data\":"+json.dumps(list(review_obj))+"}"
		# data = "{\"review_data\":"+json.dumps(list(review_obj))+",\"page_total\":\""+str(page_total)+"\",\"items_total\":\""+str(items_obj.count())+"\"}"
		return HttpResponse(data)

