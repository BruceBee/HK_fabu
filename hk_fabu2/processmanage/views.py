# -*- coding:utf-8 -*-
from django.shortcuts import render,HttpResponse, render_to_response
#from index.models import UserLoginInfo
from usermanage.models import UserInfo
from projectinfo.models import Project
from processmanage.models import ProcessInfo
import json,os,commands,re
from django.db.models import Q



def GetUserAuth(user):
	UserObject = UserInfo.objects.get(user=user)
	return UserObject.have_publish,UserObject.have_review,UserObject.have_test

def index(request):
	have_publish,have_review,have_test = GetUserAuth(request.session['LoginName'])
	return render(request,'processmanage/process.html',{'LoginName': request.session['LoginName'],
											  'navbar':'进程管理',
											  'url':'/processmanage/',
											  'have_publish':have_publish,
											  'have_review':have_review,
											  'have_test':have_test})

GetProcessInfoCMD = '/usr/local/bin/ansible %s -a "ps aux|grep tomcat_%s |grep -v grep " -m shell' 

def AnsibleExcute(modulename):
	status, output = commands.getstatusoutput(GetProcessInfoCMD % (modulename,modulename))
	return status, output

# 获取进程信息函数
def GetProcessInfo(request):



	modulelistobj = Project.objects.filter(project_status = '1').values('project_name');
	modulelist = []
	for module in modulelistobj:
		modulelist.append(module['project_name']+';')

	# return HttpResponse(modulelist)

	modulelist = ['omweb','ucweb','payaccountmanage']
	ret =[]
	for i in range(len(modulelist)):
		status, output=AnsibleExcute(modulelist[i])
		ret.append(output)
	return HttpResponse(ret)






#前端向后端获取进程的条目(模块名列表、ip列表)
def processitems(request):

	modulelist = Project.objects.filter(project_status = '1').values('project_name');
	iplist = []
	for i in Project.objects.filter(project_status = '1'):
		server_count = len(i.project_server.split(';'))-1
		for j in range(server_count):
			iplist.append(i.project_server.split(';')[j])
	if request.method == 'POST':

		s_page = request.POST['s_page']
		page_size = request.POST['page_size']
		modulename = request.POST['modulename'].encode('utf-8')
		processstatus = request.POST['processstatus']
		hostip = request.POST['hostip'].encode('utf-8')
		if modulename == '全部模块':
			modulename = ''
		else:
			modulename ='tomcat_'+modulename
		if processstatus == 'A':
			processstatus = ''
		if hostip == '全部IP':
			hostip = ''


		# modulename = ''
		# hostip = ''
		# processstatus = ''

		processitems = ProcessInfo.objects.filter(COMMAND__contains=str(modulename),HostIP__contains=str(hostip),STAT__contains=str(processstatus)).values().order_by('-id')[(int(s_page)-1)*int(page_size):int(s_page)*int(page_size)]
	# else:
	# 	processitems = ProcessInfo.objects.all().values()

	# data = "{\"review_data\":"+json.dumps(list(review_obj))+",\"page_total\":"+str(page_total)+"}"
	# data = "{\"modulelist\":"+json.dumps(list(modulelist))+"}"
		data = "{\"modulelist\":"+json.dumps(list(modulelist))+",\"processitems\":"+json.dumps(list(processitems))+",\"iplist\":"+json.dumps(list(set(iplist)))+"}"
		return HttpResponse(data)


def processitemscount(request):
	page_total = ProcessInfo.objects.all().count()
	return HttpResponse(page_total)

#前端向后端获取进程的数量
def processearchcount(request):
	modulename = request.POST['modulename'].encode('utf-8')
	processstatus = request.POST['processstatus']
	hostip = request.POST['hostip'].encode('utf-8')
	isupdatenow = request.POST['isupdatenow']
	if modulename == '全部模块':
		modulename = ''
	else:
		modulename ='tomcat_'+modulename
	if processstatus == 'A':
		processstatus = ''
	if hostip == '全部IP':
		hostip = ''
	
	CMD = '/usr/local/bin/python /home/fabu/hk_fabu2/processmanage/psupdate.py'
	'''
	当isupdatenow参数传递的值为updatenow时即触发后端同步动作
	'''

	if isupdatenow == 'updatenow':

		status, output = commands.getstatusoutput(CMD)
		# return HttpResponse(output)

		search_total = ProcessInfo.objects.filter(COMMAND__contains=str(modulename),HostIP__contains=str(hostip),STAT__contains=str(processstatus)).count()
		return HttpResponse(search_total)
	else:
		search_total = ProcessInfo.objects.filter(COMMAND__contains=str(modulename),HostIP__contains=str(hostip),STAT__contains=str(processstatus)).count()
		return HttpResponse(search_total)
	
	# search_total = ProcessInfo.objects.filter(COMMAND__contains=str(modulename),HostIP__contains=str(hostip),STAT__contains=str(processstatus)).count()
	# return HttpResponse(search_total)




