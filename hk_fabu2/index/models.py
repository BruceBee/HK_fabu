# -*- coding=utf-8 -*-
from __future__ import unicode_literals
from django.db import models


class UserLoginInfo(models.Model):
    user = models.CharField(max_length=16, primary_key=True)      # 账号
    password = models.CharField(max_length=32)        # 密码
    ftp_path = models.CharField(max_length=200)     # ftp主目录
    remark = models.CharField(max_length=200)     # 备注
    #have_publish：是否有发布权限，0-没有，1-有
    have_publish = models.CharField(max_length=4,default="1")
    #have_publish：是否有审核权限，0-没有，1-有
    have_review = models.CharField(max_length=4,default="1")
    #have_test：是否有测试权限，0-没有，1-有
    have_test = models.CharField(max_length=4,default='1')


class Logging(models.Model):
    ctime = models.DateTimeField(auto_now_add=True)       # 创建时间
    operation = models.CharField(max_length=20)     # 操作类型 部署：Deployment 项目修改：ModefyProject 启停：StartStopRestart
    state = models.CharField(max_length=10)     # 发布完成状态
    user = models.CharField(max_length=16)      # 账号
    project_name = models.CharField(max_length=200)     # 项目名
    dest_server = models.CharField(max_length=200)      # 目标服务器
    deployment_pack = models.CharField(max_length=100, null=True)
    log_date = models.TextField()    # 日志内容


class PublishInfo(models.Model):
    publish_state = models.CharField(max_length=10,default='审核中')
    publish_module = models.CharField(max_length=30)
    publish_filename = models.CharField(max_length=30)
    publish_user = models.CharField(max_length=16)  #发布者

