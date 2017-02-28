#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import unicode_literals
from django.db import models


class Project(models.Model):
    project_name = models.CharField(max_length=60, primary_key=True)        # 项目模块名
    project_server = models.CharField(max_length=300)       # 项目模块部署的服务器IP列表
    project_msg = models.CharField(max_length=999, null=True)       # 项目模块说明
    project_port = models.IntegerField()
    create_time = models.CharField(max_length=32, default='0000-00-00 00:00:00')
    create_user = models.CharField(max_length=16, default='-')
    update_time = models.CharField(max_length=32,blank=True,null=True)
    update_user = models.CharField(max_length=32,blank=True,null=True)
    '''
    project_status:
    0-已停用
    1-已启用
    '''
    project_status = models.CharField(max_length=4, default='1')

class Server(models.Model):
    server_name = models.CharField(max_length=60)
    server_ip = models.CharField(max_length=16)
    ssh_port = models.CharField(max_length=8)
    root_passwd = models.CharField(max_length=16)
    server_remark = models.CharField(max_length=60)
    create_time = models.CharField(max_length=32, default='0000-00-00 00:00:00')
    create_user = models.CharField(max_length=16, default='-')
    update_time = models.CharField(max_length=32,blank=True,null=True)
    update_user = models.CharField(max_length=32,blank=True,null=True)
    '''
    server_status:
    0-已停用
    1-已启用
    '''   
    server_status = models.CharField(max_length=4, default='1')