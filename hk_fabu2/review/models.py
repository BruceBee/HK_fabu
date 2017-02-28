#_*_coding:utf-8_*_
from django.db import models

# Create your models here.

class ForReview(models.Model):
	'''
	publish_status以下几种状态：
	0:待审核
	1:审核通过，发布完成
	2:审核不通过，未发布
	'''

	publish_status = models.CharField(max_length=20,default=u'待审核')
	publish_type = models.CharField(max_length=20,default=u'增量部署')
	publish_module = models.CharField(max_length=30)
	publish_filename = models.CharField(max_length=30)
	file_uploadtime = models.CharField(max_length=30,default='00-00-00 00:00:00')
	publish_user = models.CharField(max_length=16)
	review_owner = models.CharField(max_length=30,default='-')
	# create_time = models.DateTimeField(auto_now_add=True)
	create_time = models.CharField(max_length=30)
	publish_serverlist = models.CharField(max_length=256)
	publish_detail = models.TextField(max_length=1024,default='')
	'''
	is_active是否为活跃
	0-活跃
	1-不活跃
	'''
	is_active = models.CharField(max_length=2,default='0')
	update_user = models.CharField(max_length=16,blank=True,null=True)


class ReviewAction(models.Model):
	publish_id = models.CharField(max_length=30)
	'''
	publish_status:
		0:审核通过，发布完成
		1:审核不通过，未发布
	'''
	publish_status = models.CharField(max_length=30)
	publish_type = models.CharField(max_length=30,default=u'增量部署')
	publish_module = models.CharField(max_length=30)
	publish_filename = models.CharField(max_length=30)
	file_uploadtime = models.CharField(max_length=30,default='00-00-00 00:00:00')
	publish_user = models.CharField(max_length=16)
	create_time = models.CharField(max_length=30)
	publish_serverlist = models.CharField(max_length=256)
	publish_detail = models.TextField(max_length=1024,default='-')
	review_owner = models.CharField(max_length=30)
	review_time = models.CharField(max_length=30)
	review_info = models.TextField(max_length=1024)

	publish_strtime = models.CharField(max_length=30,blank=True,null=True,default='00-00-00 00:00:00')
	publish_endtime = models.CharField(max_length=30,blank=True,null=True,default='00-00-00 00:00:00')
	'''
	is_active是否为活跃
	0-活跃
	1-不活跃
	'''
	is_active = models.CharField(max_length=2,default='0')
	update_user = models.CharField(max_length=16,blank=True,null=True)


