#_*_coding:utf-8_*_
from django.db import models

# Create your models here.
class SoftwareTest(models.Model):
	publish_id = models.CharField(max_length=30)
	'''
	publish_status:
		0:审核通过，发布完成
		1:审核不通过，未发布
	'''
	publish_status = models.CharField(max_length=30,default='-')
	publish_type = models.CharField(max_length=30,default=u'增量部署')
	publish_module = models.CharField(max_length=30,default='-')
	publish_filename = models.CharField(max_length=30,default='-')
	file_uploadtime = models.CharField(max_length=30,default='00-00-00 00:00:00')
	publish_user = models.CharField(max_length=16,default='-')
	create_time = models.CharField(max_length=30,default='-')
	publish_serverlist = models.CharField(max_length=256,default='-')
	publish_detail = models.TextField(max_length=1024,default='-')
	review_owner = models.CharField(max_length=30,default='-')
	review_time = models.CharField(max_length=30,default='-')
	review_info = models.TextField(max_length=1024,default='-')

	publish_strtime = models.CharField(max_length=30,blank=True,null=True,default='00-00-00 00:00:00')
	publish_endtime = models.CharField(max_length=30,blank=True,null=True,default='00-00-00 00:00:00')

	test_user = models.CharField(max_length=30,blank=True,null=True)
	test_starttime = models.CharField(max_length=30,blank=True,null=True)
	test_endtime = models.CharField(max_length=30,blank=True,null=True)
	test_detail = models.TextField(max_length=4096,blank=True,null=True)
	'''
	test_status以下几种状态：
	0:待测试
	1:测试完成，通过
	2:测试完成，不通过
	3:其他
	'''
	test_status = models.CharField(max_length=4,default='0')
	'''
	is_active是否为活跃
	0-活跃
	1-不活跃
	'''
	is_active = models.CharField(max_length=2,default='0')
	update_user = models.CharField(max_length=16,blank=True,null=True)

