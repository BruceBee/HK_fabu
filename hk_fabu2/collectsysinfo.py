#!/usr/bin/env python
# -*- coding:utf-8 -*-
import commands
import json


status, output = commands.getstatusoutput('ansible 10.0.0.106 -m setup')

# print status

# print output.split('SUCCESS => ')[1]
# print type(output.split('SUCCESS => ')[1])


param = json.loads(output.split('SUCCESS => ')[1])
# print param['ansible_facts']['ansible_distribution']

'''
#获取ip
for i in range(len(param['ansible_facts']['ansible_all_ipv4_addresses'])):
	print param['ansible_facts']['ansible_all_ipv4_addresses'][i]
'''


# for j in range(len(param['ansible_facts']['ansible_memory_mb'])):
# 	print param['ansible_facts']['ansible_memory_mb']
	# for k in range(len(param['ansible_facts']['ansible_memory_mb'][j])):
	# 	print param['ansible_facts']['ansible_memory_mb'][j][k]

# for k,v in enumerate(param['ansible_facts']['ansible_memory_mb']):
# 	print k,v,param['ansible_facts']['ansible_memory_mb'][k]
# 	for kk,vv in enumerate(param['ansible_facts']['ansible_memory_mb'][v]):
# 		print kk,vv



#获取内存
for k,v in enumerate(param['ansible_facts']['ansible_memory_mb']):
	# print k,v,param['ansible_facts']['ansible_memory_mb'][v]
	for kk,vv in enumerate(param['ansible_facts']['ansible_memory_mb'][v]):
		print v,vv,param['ansible_facts']['ansible_memory_mb'][v][vv]


'''
#获取硬盘
for k,v in enumerate(param['ansible_facts']['ansible_mounts']):
	print '-----'
	for kk,vv in enumerate(v):
		if vv in ['size_total','size_available']:
			if int(v[vv]) / (1024*1024*1024) > 0:
				a = str(int(v[vv]) / (1024*1024*1024))+' G'
			else:
				a = str(int(v[vv]) / (1024*1024))+' M'

			
		else: a = v[vv]
		print kk,vv,a
'''


'''
结果
10.0.0.204
real total 1877
real used 1805
real free 72
swap cached 4
swap total 4095
swap used 30
swap free 4065
nocache used 1466
nocache free 411

'''