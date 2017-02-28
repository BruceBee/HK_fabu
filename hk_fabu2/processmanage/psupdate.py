# -*- coding:utf-8 -*-

import json
import os,sys
import commands
import time
import django



BASE_DIR=os.path.dirname(os.getcwd())
#tomcat账号调用该脚本时候，得到的BASE_DIR是/home
sys.path.append(BASE_DIR+'/fabu/hk_fabu2')

sys.path.append('/home/fabu/hk_fabu2')
# import hk_fabu2
# print sys.path
# from hk_fabu2 import settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hk_fabu2.settings")
django.setup()
from processmanage.models import ProcessInfo
from projectinfo.models import Project

GetProcessInfoCMD = '/usr/bin/ansible %s -a "ps aux|grep tomcat_%s |grep -v grep " -m shell' 

def AnsibleExcute(modulename):
	status, output = commands.getstatusoutput(GetProcessInfoCMD % (modulename,modulename))
	return status, output


def UpdateProcess():

	modulelistobj = Project.objects.filter(project_status = '1').values('project_name');
	modulelist = []
	for module in modulelistobj:
		modulelist.append(module['project_name'][1:-1])

	print modulelist

	# return HttpResponse(modulelist)

	# modulelist = ['omweb','ucweb','payaccountmanage','analysisjob','analysis','bmjAppPay','common','hkweb','hykClient','maClient','order']
	# modulelist = ['omweb']
	ret =[]
	for i in range(len(modulelist)):
		print '-----'+modulelist[i]+'------'
		status, output=AnsibleExcute(modulelist[i])
		# print status,output
		'''
		status:0或者512,整个操作只会返回一个status，这个status对应整个output
		output:全部的输出内容
		'''
		# for k,v in enumerate(output.split('\n')):
		# 	print k,v


		for k,v in enumerate(output.split('\n')):
				
				if 'SUCCESS' in v:
					# print k,v.split(" ")[0]
					HostIP = v.split(" ")[0]
					USER =';'.join(output.split('\n')[k+1].split()).split(";")[0]
					PID =';'.join(output.split('\n')[k+1].split()).split(";")[1]
					CPU =';'.join(output.split('\n')[k+1].split()).split(";")[2]
					MEM =';'.join(output.split('\n')[k+1].split()).split(";")[3]
					START =';'.join(output.split('\n')[k+1].split()).split(";")[8]
					TIME =';'.join(output.split('\n')[k+1].split()).split(";")[9]
					COMMAND =';'.join(output.split('\n')[k+1].split()).split(";")[10:-1]
					STAT =';'.join(output.split('\n')[k+1].split()).split(";")[7]

					print HostIP,USER,PID,STAT
					ProcessInfo.objects.create(HostIP=HostIP,USER=USER,PID=PID,CPU=CPU,MEM=MEM,START=START,TIME=TIME,COMMAND=COMMAND,STAT=STAT,CollectTime=time.strftime('%Y-%m-%d %H:%M:%S'))

				elif 'FAILED' in v:
					print v.split(" ")[0]+' is FAILED!!!'

				if 'UNREACHABLE' in v:
					print v.split(" ")[0]+' is UNREACHABLE!!!'
				else:
					pass
				


		'''

		if status == 0 or status == 512:
			for k,v in enumerate(output.split('\n')):
				# print k,v
				#if k== 0 or k%2 == 0:


				
				if 'SUCCESS' in v:
					# print k,v.split(" ")[0]
					HostIP = v.split(" ")[0]
					USER =';'.join(output.split('\n')[k+1].split()).split(";")[0]
					PID =';'.join(output.split('\n')[k+1].split()).split(";")[1]
					CPU =';'.join(output.split('\n')[k+1].split()).split(";")[2]
					MEM =';'.join(output.split('\n')[k+1].split()).split(";")[3]
					START =';'.join(output.split('\n')[k+1].split()).split(";")[8]
					TIME =';'.join(output.split('\n')[k+1].split()).split(";")[9]
					COMMAND =';'.join(output.split('\n')[k+1].split()).split(";")[10:-1]
					STAT =';'.join(output.split('\n')[k+1].split()).split(";")[7]

					print HostIP,USER,PID,STAT
					# ProcessInfo.objects.create(HostIP=HostIP,USER=USER,PID=PID,CPU=CPU,MEM=MEM,START=START,TIME=TIME,COMMAND=COMMAND,STAT=STAT,CollectTime=time.strftime('%Y-%m-%d %H:%M:%S'))

				elif 'FAILED' in v:
					print v.split(" ")[0]+' is FAILED!!!'
				else:
					pass
					# print k,v

					# ProcessInfo.objects.create(HostIP=HostIP,USER=USER,PID=PID,CPU=CPU,MEM=MEM,START=START,TIME=TIME,COMMAND=COMMAND,STAT=STAT,CollectTime=time.strftime('%Y-%m-%d %H:%M:%S'))
		#状态不为0，即采集数据失败
		elif status == 1024:
			for k,v in enumerate(output.split('\n')):
				if 'UNREACHABLE' in v:
					print v.split(" ")[0]+' is UNREACHABLE!!!'

		else:
			print status,output
			for k,v in enumerate(output.split('\n')):
				print k,v

		'''

UpdateProcess()
print time.strftime('%Y-%m-%d %H:%M:%S')
