#!/usr/bin/env python
# -*- coding:utf-8 -*-
import commands
import json

status, output = commands.getstatusoutput('df -h')

# print output

# param = json.loads(output.split('SUCCESS => ')[1])

# for k,v in enumerate(param['ansible_facts']['ansible_memory_mb']):
# 	for kk,vv in enumerate(param['ansible_facts']['ansible_memory_mb'][v]):
# 		print v,vv,param['ansible_facts']['ansible_memory_mb'][v][vv]


aa = {}
for k,v in enumerate(output.split('\n')):
	print k,v
	print v.split()[0]
	aa[v.split()[0]] = [v.split()[1],v.split()[2],v.split()[3],v.split()[4],v.split()[5]]
	# for kk,vv in enumerate(v):
	# 	print kk,vv

print aa