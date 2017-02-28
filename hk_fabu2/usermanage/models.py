# -*- coding=utf-8 -*-
from django.db import models

# Create your models here.
class UserInfo(models.Model):
    user = models.CharField(max_length=16, primary_key=True)      # 账号
    password = models.CharField(max_length=32)        # 密码
    ftp_path = models.CharField(max_length=32)     # ftp主目录
    remark = models.CharField(max_length=32)     # 备注
    #have_publish：是否有发布权限，0-没有，1-有
    have_publish = models.CharField(max_length=4,default="1")
    #have_publish：是否有审核权限，0-没有，1-有
    have_review = models.CharField(max_length=4,default="1")
    #have_test：是否有测试权限，0-没有，1-有
    have_test = models.CharField(max_length=4,default='1')

    create_time = models.CharField(max_length=20,default='0000-00-00 00:00:00')
    '''
    user_status:
    0-已禁用
    1-已启用
    '''
    user_status = models.CharField(max_length=2,default='1')

    update_time = models.CharField(max_length=20,blank=True,null=True)
    update_user = models.CharField(max_length=20,blank=True,null=True)